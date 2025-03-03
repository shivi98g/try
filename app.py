
import json
import os 
from flask import Flask, jsonify, request , render_template
import torch   #pytorch facebook like Keras library h fo DL and ML
from torch.utils.data import DataLoader   #data from csv read usko into ptorch form converts

#print("Import All Successful")



#Task1
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
proposed_class_index = json.load(open('proposed_class_index.json'))

#model = models.densenet121(pretrained=True)  #####
model = torch.load('proposed_1D.pt', map_location={'cuda:0': 'cpu'})
model.eval()


proposed_class_index_doctor = json.load(open('proposed_class_index_doctor.json'))

#model = models.densenet121(pretrained=True)  #####
model_doctor = torch.load('proposed_1D_5.pt', map_location={'cuda:0': 'cpu'})
model_doctor.eval()



def get_prediction(test_data):
    batch_size = 20

 #   print("In web API ")
  #  print(test_data.__len__())
    test_data_tensor = torch.tensor(test_data, dtype=torch.float)#.unsqueeze_(0)
    test_data_tensor=test_data_tensor.view(1, 1, 178)
   # print(test_data_tensor.shape)
    test_dataloader = DataLoader(dataset=test_data_tensor, batch_size=batch_size)

    with torch.no_grad():
        for signals in test_dataloader:
            outputs = model(signals)
          #  print("output ")
    #        print(outputs)
                    #outputs = model(signals)
            y_pred = outputs.argmax(dim=1).tolist()[0]
           # print(y_pred)
            y_pred = str(y_pred)
            #print(y_pred)


            return proposed_class_index[y_pred]


def get_prediction_doctor(test_data):
    batch_size = 20

 #   print("In web API ")
  #  print(test_data.__len__())
    test_data_tensor = torch.tensor(test_data, dtype=torch.float)#.unsqueeze_(0)
    test_data_tensor=test_data_tensor.view(1, 1, 178)
   # print(test_data_tensor.shape)
    test_dataloader = DataLoader(dataset=test_data_tensor, batch_size=batch_size)

    with torch.no_grad():
        for signals in test_dataloader:
            outputs = model_doctor(signals)
          #  print("output ")
    #        print(outputs)
                    #outputs = model(signals)
            y_pred = outputs.argmax(dim=1).tolist()[0]
           # print(y_pred)
            y_pred = str(y_pred)
            #print(y_pred)


            return proposed_class_index_doctor[y_pred]



@app.route('/')
def home():
    
  return render_template('/index.html')
  


@app.route('/web', methods=['POST'])
def predict():
    if request.method == 'POST':
        #req_data = request.get_json()

        test_data = request.json["data"]# req_data['form']['data']
        #test_data = file.read()
      #  print(type(test_data))
       # print(test_data)


        class_name = get_prediction(test_data=test_data)
        #print(class_name)
        return jsonify(class_name= class_name)



@app.route('/webDoctor', methods=['POST'])
def predictDoctor():
    if request.method == 'POST':
        #req_data = request.get_json()

        test_data = request.json["data"]# req_data['form']['data']
        #test_data = file.read()
      #  print(type(test_data))
       # print(test_data)


        class_name = get_prediction_doctor(test_data=test_data)
        #print(class_name)
        return jsonify(class_name= class_name)



if __name__ == '__main__':

   # test_dataset = UCI_epilepsy('test', 'Task1')

    #X=(get_prediction(test_dataset))
    #print("Json")
    #print(type(X))
    #application.run()
    app.run()#(port=os.getenv('PORT', 8000))