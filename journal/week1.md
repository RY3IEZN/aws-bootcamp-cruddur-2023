# Week 1 — App Containerization

Following the tutorial as always... after setting up docker i got the error404 message, which is fine

![image](https://user-images.githubusercontent.com/73601265/221247442-0967d186-b11e-4bb3-8a5d-22a88855eced.png)


after setting up the env, and running this command, it works and return json(after appending /api/activities/home)

cmd:docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask

![image](https://user-images.githubusercontent.com/73601265/221248074-5df860db-f63b-43e7-b56f-c65a10a57ff3.png)

