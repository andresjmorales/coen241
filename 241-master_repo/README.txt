To recreate demo results, the main setup that needs to be completed is retrieving credentials from google cloud, and establishing a bucket. 
After that, the credentials, saved as cred.json can be used to upload files using some of the upload functions in MLdriver.py, or they can be manually uploaded into Google Cloud Storage.  
After this setup, first build and locally test the APIs using postman or a webrowser. Note the training functions wants a project name so with contents provided, use the path "/?project=data" for training the model.

If everything works well locally, we can deploy to Google Cloud, just note the ports exposed by each container as that could cause a failed deployment if google if ports are not properly configured. 

Once deployed everything should be as simple as using the right URL for predicting, and using the right URL and .json request.  

As a side node, becuase training can take a few minutes, it is reccomended to give the training container, at least 1, ideally 2 GB of memory, and cap each container to process only 1 request at a time. 