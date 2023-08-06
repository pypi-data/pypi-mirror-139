First Release: Perceptron Network    
    
    neural_network = Network()   

    training_inputs = np.array([[0,0,1,0],
                                [1,1,0,0],
                                [1,0,1,0],
                                [0,1,1,0]
                                ])

    training_outputs = np.array([[0,1,1,0]]).T

    neural_network.train(training_inputs, training_outputs, 1000)

    neural_network.run(np.array([[0,0,0,0]]))