import json
import http.client

class Client():
    def client(self, file_input, file_output, urn = '127.0.0.1:8000', route = '/convert'):
        with open(file_input) as f: # become the json file and open it
            json_data = f.read()
        
        con = http.client.HTTPConnection(urn)

        con.request('POST', route, json_data)
        response = con.getresponse()

        data_json = response.read().decode()


        obj = open(file_output, 'w')  # Create a OpenLABEL json file and write the values for the new format
        obj.write(data_json)
        obj.close
