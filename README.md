# Xtensorflow
XTensorflow

A high level tensorflow lib which can convert defined tf model to caffe and other engine;

 
    input =  tf.placeholder(tf.float32, [batch_size, 256])
    xnet = Xtensorflow(input, is_train=is_training, weight_decay=self.weight_decay, model_name=name)
    fc1 = xnet.fc_layer(0, [batch_size, 256], tf.nn.relu)
    fc2 = xnet.fc_layer(fc1, [batch_size, 128], tf.nn.relu)
    fc3 = xnet.fc_layer(fc2, [batch_size, self.classnum], None)
    output = xnet.get_network_output()
    
    
    
    
