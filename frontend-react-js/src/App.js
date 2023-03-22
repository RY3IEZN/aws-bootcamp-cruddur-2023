import './App.css';

import HomeFeedPage from './pages/HomeFeedPage';
import NotificationsFeedPage from './pages/NotificationsFeedPage';
import UserFeedPage from './pages/UserFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import React from 'react';
import process from 'process';
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": "eu-west-2",
  "aws_cognito_region": "eu-west-2",
  "aws_user_pools_id": "eu-west-2_Ikmv23YeQ",
  "aws_user_pools_web_client_id": "3uufg6dbjipk6ofi13drlou52s",
  "oauth": {},
  Auth: {
    // We are not using an Identity Pool
    // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
    region: "eu-west-2",           // REQUIRED - Amazon Cognito Region
    userPoolId: "eu-west-2_Ikmv23YeQ",         // OPTIONAL - Amazon Cognito User Pool ID
    userPoolWebClientId: "3uufg6dbjipk6ofi13drlou52s",   // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
  }
});


const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
  {
    path: "/messages/@:handle",
    element: <MessageGroupPage />
  },
  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />
  },
  {
    path: "/forgot",
    element: <RecoverPage />
  },
  {
    path: "/notifications",
    element: <NotificationsFeedPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;