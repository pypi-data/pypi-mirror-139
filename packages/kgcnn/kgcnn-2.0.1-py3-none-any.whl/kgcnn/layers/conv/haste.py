import tensorflow as tf
try:
    import haste_tf as haste
except ModuleNotFoundError:
    print("ERROR:kgcnn: Could not load haste implementation of GRU. Please check https://github.com/lmnt-com/haste.")
    import haste_tf as haste

from kgcnn.layers.base import GraphBaseLayer
from kgcnn.layers.modules import DenseEmbedding, ActivationEmbedding, LazyConcatenate
from kgcnn.layers.gather import GatherState
from kgcnn.layers.pooling import PoolingNodes
from kgcnn.layers.conv.attention import PoolingNodesAttention


@tf.keras.utils.register_keras_serializable(package='kgcnn', name='HasteGRUUpdate')
class HasteGRUUpdate(GraphBaseLayer):
    """Gated Recurrent Unit update with a GRU cell implementation from `haste <https://github.com/lmnt-com/haste>`_ .

    Args:
        units (int): Units for GRU cell.
        trainable (bool): If GRU is trainable. Defaults to True.
    """

    def __init__(self, units, trainable: bool = True, **kwargs):
        """Initialize layer."""
        super(HasteGRUUpdate, self).__init__(trainable=trainable, **kwargs)
        self.units = units
        self.gru_cell = haste.GRUCell(units, trainable=trainable)

    def build(self, input_shape):
        """Build layer."""
        super(HasteGRUUpdate, self).build(input_shape)
        assert len(input_shape) == 2

    def call(self, inputs, **kwargs):
        """Forward pass. Operates on values without checking splits of the ragged dimension.

        Args:
            inputs (list): [nodes, updates]

                - nodes (tf.RaggedTensor): Node embeddings of shape (batch, [N], F)
                - updates (tf.RaggedTensor): Matching node updates of shape (batch, [N], F)

        Returns:
           tf.RaggedTensor: Updated nodes of shape (batch, [N], F)
        """
        self.assert_ragged_input_rank(inputs)
        n, npart = inputs[0].values, inputs[0].row_splits
        eu, _ = inputs[1].values, inputs[1].row_splits
        out, _ = self.gru_cell(eu, n, **kwargs)
        out = tf.RaggedTensor.from_row_splits(out, npart, validate=self.ragged_validate)
        return out

    def get_config(self):
        """Update layer config."""
        config = super(HasteGRUUpdate, self).get_config()
        config.update({"units": self.units})
        return config


@tf.keras.utils.register_keras_serializable(package='kgcnn', name='HasteLayerNormGRUUpdate')
class HasteLayerNormGRUUpdate(GraphBaseLayer):
    """Gated Recurrent Unit update with a GRU cell implementation from `haste <https://github.com/lmnt-com/haste>`_
    that uses also a layer normalization.

    Args:
        units (int): Units for GRU cell.
        dropout (float): The amount of dropout to use. Default is 0.0.
        forget_bias (float): The forget bias in GRU cell. Default is 1.0.
        trainable (bool): If GRU is trainable. Defaults to True.
    """

    def __init__(self, units: int, trainable: bool = True,
                 forget_bias: float = 1.0,
                 dropout: float = 0.0,
                 **kwargs):
        """Initialize layer."""
        super(HasteLayerNormGRUUpdate, self).__init__(trainable=trainable, **kwargs)
        self.units = units
        self.gru_dropout = dropout
        self.forget_bias = forget_bias

        self.gru_cell = haste.LayerNormGRUCell(units, forget_bias=forget_bias, dropout=dropout, trainable=trainable)

    def build(self, input_shape):
        """Build layer."""
        super(HasteLayerNormGRUUpdate, self).build(input_shape)
        assert len(input_shape) == 2

    def call(self, inputs, **kwargs):
        """Forward pass. Operates on values without checking splits of the ragged dimension.

        Args:
            inputs (list): [nodes, updates]

                - nodes (tf.RaggedTensor): Node embeddings of shape (batch, [N], F)
                - updates (tf.RaggedTensor): Matching node updates of shape (batch, [N], F)

        Returns:
           tf.RaggedTensor: Updated nodes of shape (batch, [N], F)
        """
        self.assert_ragged_input_rank(inputs)
        n, npart = inputs[0].values, inputs[0].row_splits
        eu, _ = inputs[1].values, inputs[1].row_splits
        out, _ = self.gru_cell(eu, n, **kwargs)
        return tf.RaggedTensor.from_row_splits(out, npart, validate=self.ragged_validate)

    def get_config(self):
        """Update layer config."""
        config = super(HasteLayerNormGRUUpdate, self).get_config()
        config.update({"units": self.units, "forget_bias": self.forget_bias, "dropout": self.gru_dropout})
        return config


@tf.keras.utils.register_keras_serializable(package='kgcnn', name='HastePoolingNodesAttentiveLayerNorm')
class HastePoolingNodesAttentiveLayerNorm(GraphBaseLayer):
    r"""Computes the attentive pooling for node embeddings for
    `Attentive FP <https://doi.org/10.1021/acs.jmedchem.9b00959>`_ model but uses the
    `haste <https://github.com/lmnt-com/haste>`_  GRU cell as update with a layer normalization.

    Args:
        units (int): Units for the linear trafo of node features before attention.
        pooling_method(str): Initial pooling before iteration. Default is "sum".
        depth (int): Number of iterations for graph embedding. Default is 3.
        activation (str): Activation. Default is {"class_name": "kgcnn>leaky_relu", "config": {"alpha": 0.2}}.
        activation_context (str): Activation function for context. Default is "elu".
        use_bias (bool): Use bias. Default is True.
        kernel_regularizer: Kernel regularization. Default is None.
        bias_regularizer: Bias regularization. Default is None.
        activity_regularizer: Activity regularization. Default is None.
        kernel_constraint: Kernel constrains. Default is None.
        bias_constraint: Bias constrains. Default is None.
        kernel_initializer: Initializer for kernels. Default is 'glorot_uniform'.
        bias_initializer: Initializer for bias. Default is 'zeros'.
    """

    def __init__(self,
                 units,
                 depth=3,
                 pooling_method="sum",
                 activation='kgcnn>leaky_relu',
                 activation_context="elu",
                 use_bias=True,
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 activity_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 dropout=0.0,
                 forget_bias=1.0,
                 trainable=True,
                 **kwargs):
        """Initialize layer."""
        super(HastePoolingNodesAttentiveLayerNorm, self).__init__(trainable=trainable, **kwargs)
        self.pooling_method = pooling_method
        self.depth = depth
        self.units = int(units)
        kernel_args = {"use_bias": use_bias, "kernel_regularizer": kernel_regularizer,
                       "activity_regularizer": activity_regularizer, "bias_regularizer": bias_regularizer,
                       "kernel_constraint": kernel_constraint, "bias_constraint": bias_constraint,
                       "kernel_initializer": kernel_initializer, "bias_initializer": bias_initializer}
        gru_args = {"dropout": dropout, "forget_bias": forget_bias, "trainable": trainable}

        self.lay_linear_trafo = DenseEmbedding(units, activation="linear", **kernel_args)
        self.lay_alpha = DenseEmbedding(1, activation=activation, **kernel_args)
        self.lay_gather_s = GatherState()
        self.lay_concat = LazyConcatenate(axis=-1)
        self.lay_pool_start = PoolingNodes(pooling_method=self.pooling_method)
        self.lay_pool_attention = PoolingNodesAttention()
        self.lay_final_activ = ActivationEmbedding(activation=activation_context)
        self.lay_gru = haste.LayerNormGRUCell(units, **gru_args)

    def build(self, input_shape):
        """Build layer."""
        super(HastePoolingNodesAttentiveLayerNorm, self).build(input_shape)

    def call(self, inputs, **kwargs):
        """Forward pass.

        Args:
            inputs: nodes

                - nodes (tf.RaggedTensor): Node features of shape (batch, [N], F)

        Returns:
            tf.Tensor: Hidden tensor of pooled node attentions of shape (batch, F).
        """
        node = inputs

        h = self.lay_pool_start(node, **kwargs)
        wn = self.lay_linear_trafo(node, **kwargs)
        for _ in range(self.depth):
            hv = self.lay_gather_s([h, node], **kwargs)
            ev = self.lay_concat([hv, node], **kwargs)
            av = self.lay_alpha(ev, **kwargs)
            cont = self.lay_pool_attention([wn, av], **kwargs)
            cont = self.lay_final_activ(cont, **kwargs)
            h, _ = self.lay_gru(cont, h, **kwargs)

        out = h
        return out

    def get_config(self):
        """Update layer config."""
        config = super(HastePoolingNodesAttentiveLayerNorm, self).get_config()
        config.update({"units": self.units, "depth": self.depth, "pooling_method": self.pooling_method})
        conf_sub = self.lay_alpha.get_config()
        for x in ["kernel_regularizer", "activity_regularizer", "bias_regularizer", "kernel_constraint",
                  "bias_constraint", "kernel_initializer", "bias_initializer", "activation", "use_bias"]:
            config.update({x: conf_sub[x]})
        conf_context = self.lay_final_activ.get_config()
        config.update({"activation_context": conf_context["activation"]})
        conf_gru = self.lay_gru.get_config()
        for x in ["dropout", "forget_bias", "trainable"]:
            config.update({x: conf_gru[x]})
        return config
