# Week 1 — App Containerization

Following the tutorial as always... after setting up docker i got the error404 message, which is fine

![image](https://user-images.githubusercontent.com/73601265/221247442-0967d186-b11e-4bb3-8a5d-22a88855eced.png)


after setting up the env, and running this command, it works and return json(after appending /api/activities/home)

cmd:docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask

![image](https://user-images.githubusercontent.com/73601265/221248074-5df860db-f63b-43e7-b56f-c65a10a57ff3.png)

Frontend works smooth like a charm.

![image](https://user-images.githubusercontent.com/73601265/221248374-c64fa799-70d3-4f33-8d3c-16a9d49485d6.png)

so now its time to do docker compose, combine them and watch them work together

before then let me push to docker hub

this resource really helped me to learn how to push to docker hub long ago and i always refer to it anytime i cant remember off head
https://jsta.github.io/r-docker-tutorial/04-Dockerhub.html

pushed to docker hub
![image](https://user-images.githubusercontent.com/73601265/221343894-e75ec0df-c3cd-4f49-89f7-ac03dc91777c.png)
![image](https://user-images.githubusercontent.com/73601265/221343907-066b0a8e-0e68-44b8-86e5-1bb2de3d5f53.png)
![image](https://user-images.githubusercontent.com/73601265/221343971-f50ac154-1a5e-4cad-a68b-4971152ef175.png)

after working on docker compose, both containers can now communicate together the app now works

![image](https://user-images.githubusercontent.com/73601265/221356624-450e18fe-e917-4e8f-b329-74ce236ebc28.png)
![image](https://user-images.githubusercontent.com/73601265/221356713-a32cb6f5-b216-4b8d-aabc-84e583f62d8f.png)

#add postgres and dynamodb to the docker compose 

![image](https://user-images.githubusercontent.com/73601265/221359401-76a40672-f592-423a-b27d-d5b0c96d4801.png)

worked on the adding the endpoints for the backend and frontend
the backend endpoint is api/activities/notifications , which resturns json
![image](https://user-images.githubusercontent.com/73601265/222828853-fe20e1c0-4d17-4aac-8794-d31ca2b071bb.png)

the front end adds the notification tab to the left hand side, (you need to be logged in to see it)
all this is the picture after its done and bothe FE and BE arw communicating

![Uploading image.png…]()

THank you very much... moving to week 2

