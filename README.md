**MNIST Sign Language** project involves building a Convolutional Neural Network (CNN) to classify images of hand gestures into corresponding sign language letters.

---

## Model Architecture

The CNN is designed to process $28\times28$ grayscale images. It uses a structured approach to extract features and classify them:

* **Input Layer**: Accepts $28\times28\times1$ normalized image tensors.


* **Convolutional Layers**:
* **Layer 1**: 64 filters ($3\times3$ kernel), ReLU activation, and valid padding.


* **Layer 2**: 128 filters ($3\times3$ kernel) to extract more complex spatial features.




* **Pooling Layers**: MaxPooling2D with a $2\times2$ pool size is used after each convolution to reduce spatial dimensions by half.


* **Dropout Layers**: Applied after pooling and dense layers to prevent overfitting by randomly dropping neurons during training (30%, 40%, and 50% rates respectively).


* **Dense & Output Layers**: A fully connected layer with 256 neurons feeds into a final output layer using **Softmax activation** to produce probabilities for each gesture class.



---

## Workflow & Performance

The project followed a standard machine learning pipeline:

* **Data Preparation**: Images were normalized to a range of 0 to 1, and labels were **one-hot encoded** into binary vectors.


* **Training**: The model was trained using the **Adam optimizer** and **categorical cross-entropy loss**. It ran for up to 50 epochs with a batch size of 128.


* **Results**: The model achieved an impressive **96% accuracy** on the test set.


* **Overfitting Prevention**: Regularization techniques like dropout and early stopping were critical in ensuring the model generalized well to unseen data.



---

## Key Concepts Explained

### ReLU vs. Sigmoid Activation

| Feature | ReLU 

 | Sigmoid 

 |
| --- | --- | --- |
| **Output Range** | 0 to $\infty$ 

 | 0 to 1 

 |
| **Convergence** | Faster due to non-saturation for positive inputs 

 | Slower 

 |
| **Main Advantage** | Avoids the vanishing gradient problem 

 | Ideal for modeling probabilities 

 |

### One-Hot Encoding

This technique converts categorical labels (like "Apple" or "Orange") into a numerical format. Each category becomes a binary feature, allowing the neural network to clearly distinguish between classes without implying any mathematical order between them.

Would you like to see the specific calculation for how the dimensions change after the convolution and pooling layers?