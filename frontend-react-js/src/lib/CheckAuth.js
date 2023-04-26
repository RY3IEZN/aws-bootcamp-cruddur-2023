import { Auth } from 'aws-amplify';

const checkAuth = async (setUser) => {
  Auth.currentAuthenticatedUser({
    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((cognito_user) => {
    console.log('user',cognito_user);
    setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
    return Auth.currentSession()
    // return Auth.currentAuthenticatedUser()
}).then((cognito_user_session) => {
      console.log('userssssss',cognito_user_session);
      localStorage.setItem("access_token", user.accessToken.jwtToken)
  })
  .catch((err) => console.log(err));
};

export default checkAuth;