# djhautomodel

Automated machine learning software to simplify the machine learning development and deployment with user friendliness and ease of integration developed with django framework.


# Youtube video demo
https://youtu.be/YtnySoWzuhE


# TRY IT OUT
docker run -p 8000:8000 dabidinjr/djhautomodel

Browse to http://0.0.0.0:8000/ and login using credentials below.

username: admin
password: admin


# You can also Clone and build and Run
Clone the repository and run the following in same directory as the Dockerfile

$docker build --tag djhautomodel .

$docker run -p 8000:8000 -it --name mydjhautomodel djhautomodel


# API Endpoints
'api-token-auth/' = Generate token to call other apis

'api/' = Base api DRF router

'api/train_sd/' = Train structure data classifier or regressor

'api/predict_sd/' =  Predict structure data classifier or regressor

'api/automlmodel' = AutoML Model queryset GET PUT DELETE UPDATE. But no CREATE/POST new.
