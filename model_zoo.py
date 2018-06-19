import tensorflow as tf
from Xtensorflow import Xtensorflow


def Resnet50(input, batch_size, name, reuse = False ,model_path = None):
    with tf.variable_scope(name) as scope:
        if reuse:
            tf.get_variable_scope().reuse_variables()
        else:
            assert tf.get_variable_scope().reuse == False


        def resnet_block(input_index, input_shape, is_botteneck = False):
            input_dim = input_shape[-1]

            if not is_botteneck:
                scale0 = xnet.bn_with_scale_layer(input_index, tf.nn.relu, index=input_index + 1)
                conv1 = xnet.conv_with_bn_layer(scale0, [batch_size, input_dim/4], 1, 1, tf.nn.relu, index=scale0 + 1)
                conv2 = xnet.conv_with_bn_layer(conv1, [batch_size, input_dim/4], 3, 1, tf.nn.relu, index=conv1 + 1)
                conv3 = xnet.conv_with_bn_layer(conv2, [batch_size, input_dim], 1, 1, None, index=conv2 + 1)
                out = xnet.sum_layer([conv3, input_index], index=conv3 + 1, activation=None)

            else:
                scale0 = xnet.bn_with_scale_layer(input_index, tf.nn.relu, index=input_index + 1)
                conv1 = xnet.conv_with_bn_layer(scale0, [batch_size, input_dim/2], 1, 1, tf.nn.relu, index=scale0 + 1)
                conv2 = xnet.conv_with_bn_layer(conv1, [batch_size, input_dim/2], 3, 2, tf.nn.relu, index=conv1 + 1)
                conv3 = xnet.conv_with_bn_layer(conv2, [batch_size, input_dim*2], 1, 1, None, index=conv2 + 1)

                conv_sc = xnet.conv_with_bn_layer(scale0, [batch_size, input_dim * 2], 1, 2, None, index=conv3 + 1)
                out = xnet.sum_layer([conv3, conv_sc], index=conv_sc + 1, activation=None)

            return out

        xnet = Xtensorflow(input ,model_name = name, load_from_txt = model_path)
        conv1 = xnet.conv_with_bn_layer(0, [batch_size, 128], 7, 2, tf.nn.relu, index=1)
        pool2 = xnet.maxpooling_layer(conv1,[batch_size, 128], 3, 2, index=conv1 + 1)

        # first_unit
        first_unit_conv1 = xnet.conv_with_bn_layer(pool2, [batch_size, 128], 1, 1, tf.nn.relu, index=pool2 + 1)
        first_unit_conv2 = xnet.conv_with_bn_layer(first_unit_conv1, [batch_size, 128], 3, 1, tf.nn.relu, index=first_unit_conv1 + 1)
        first_unit_conv3 = xnet.conv_with_bn_layer(first_unit_conv2, [batch_size, 256], 1, 1, None, index=first_unit_conv2+1)

        first_unit_sc = xnet.conv_with_bn_layer(first_unit_conv1, [batch_size, 256], 1, 1, None, index=first_unit_conv3 + 1)
        first_unit_plus_0 = xnet.sum_layer([first_unit_conv3, first_unit_sc], index=first_unit_sc + 1, activation=None)

        # stage1
        stage1_unit2= resnet_block(first_unit_plus_0, [batch_size, 256], is_botteneck=False)
        stage1_unit3 = resnet_block(stage1_unit2, [batch_size, 256], is_botteneck=False)

        # stage2
        stage2_unit1= resnet_block(stage1_unit3, [batch_size, 256], is_botteneck=True)
        stage2_unit2 = resnet_block(stage2_unit1, [batch_size, 512], is_botteneck=False)
        stage2_unit3 = resnet_block(stage2_unit2, [batch_size, 512], is_botteneck=False)
        stage2_unit4 = resnet_block(stage2_unit3, [batch_size, 512], is_botteneck=False)

        # stage3
        stage3_unit1= resnet_block(stage2_unit4, [batch_size, 512], is_botteneck=True)
        stage3_unit2 = resnet_block(stage3_unit1, [batch_size, 1024], is_botteneck=False)
        stage3_unit3 = resnet_block(stage3_unit2, [batch_size, 1024], is_botteneck=False)
        stage3_unit4 = resnet_block(stage3_unit3, [batch_size, 1024], is_botteneck=False)
        stage3_unit5 = resnet_block(stage3_unit4, [batch_size, 1024], is_botteneck=False)
        stage3_unit6 = resnet_block(stage3_unit5, [batch_size, 1024], is_botteneck=False)

        # stage4
        stage4_unit1= resnet_block(stage3_unit6, [batch_size, 1024], is_botteneck=True)
        stage4_unit2 = resnet_block(stage4_unit1, [batch_size, 2048], is_botteneck=False)
        stage4_unit3 = resnet_block(stage4_unit2, [batch_size, 2048], is_botteneck=False)

        final_scale = xnet.scale_layer(stage4_unit3, None, index=stage4_unit3 + 1)
        # final_fc = xnet.fc_layer(final_scale, [batch_size, 512], None)

    return xnet.get_network_output(), xnet

if __name__ == '__main__':
    input = tf.placeholder(tf.float32, [None, 224, 224, 1])
    Resnet50(input, None, name='resnet50')