<h1>CSCI630 - Lab 3</h1>
<h2>Language Classifier using Decision Tree.</h2>
<br>

investigating the use of decision trees and boosted decision stumps to
classify text as one of two languages. The task is to collect data and train 
(in several ways) some decision stumps/trees so that when given a 15 word segment of text from either the
English or Dutch Wikipedia, the code will state to the best of its ability 
which language the text is in.

<h4>Execution instructions -</h4>
<ol>
    <li>Training a model -</li>

        python lab3.py train training_samples.dat training_model.model 
        training_method

        Where ->
        1. training_samples.dat - Training data with labels
        2. training_model.model - Training model
        3. training_method - "dt"/"ada", train using decision trees or adaboost


<li>Predicting using a model -</li>

        python lab3.py predict training_model.model test_data.dat
        
        Where ->
        1. training_model.model - Model created during training with type 
        either "dt" or "ada".
        2. test.dat - Testing data

</ol>

<b>Note -</b>
The Adaboost part of the code is incomplete and a work in progress.<br>
The decision tree testing was succesfull and all test cases passed.<br>
Use train.dat to train the model and test.dat to check the results of 
prediction for a smaller dataset.