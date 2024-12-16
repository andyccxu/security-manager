# Security Management Service

This service manages authentication and authorization by issuing JSON Web Tokens (JWTs) with specific scope grants.  It provides a secure way to verify user identity through Google login and subsequently grants access to various application resources.

## Features

* **Token Exchange:**  Exchanges a Google ID Token for a service-specific JWT. This allows users to authenticate with Google and then use the generated JWT for seamless access to authorized resources within the application ecosystem.
* **Scope-Based Authorization:**  JWTs issued by this service include scope grants. These scopes define the permissions a user has within the application.  This allows for granular control over access to different features and resources.
* **Secure Token Generation:**  Utilizes strong encryption practices (HS256 algorithm) and securely stores the signing secret key in Google Secret Manager to ensure the integrity and confidentiality of issued tokens.

## API Endpoint

The service exposes a single endpoint for token exchange:

* **GET `/exchange_token_with_google_id`**:  Accepts a Google ID Token and Client ID in the request headers. Upon successful verification, it generates a JWT with defined scopes and returns it along with the user information retrieved from Google.  If verification fails, it returns an appropriate error response.  Requires the following headers:
    * `google_id_token`: The ID token received from Google Sign-In.
    * `client_id`: The client ID of your Google application.

## Setup and Deployment

This service is deployed to Google Cloud Run.

1. **Secret Management:**  Store the JWT signing secret key securely in Google Secret Manager. This key is accessed by the service during token generation. Name this secret `SECURITY_MANAGER_SECRET_KEY` within a project.
2. **Google Client ID:**  Obtain a client ID for your Google application. This is required for verifying the Google ID Token.  Ensure that the appropriate OAuth 2.0 scopes are configured for your Google application.
3. **CORS Configuration:** Configure Cross-Origin Resource Sharing (CORS) to allow requests from your frontend application's origin.


## Usage

The typical flow for using the service is as follows:

1. **Frontend Authentication:** The frontend application performs user authentication with Google Sign-In.
2. **Token Exchange:** Upon successful Google authentication, the frontend sends the received Google ID Token and the Google Client ID to the `/exchange_token_with_google_id` endpoint of this service.
3. **JWT Generation:** The service verifies the Google ID Token and, if valid, generates a JWT with the appropriate scopes.
4. **Authorized Access:** The frontend receives the JWT and includes it in subsequent requests to protected resources.  Backend services can then validate the JWT and authorize access based on the included scopes.


## Example Response:

```json
// response in JSON format
{
  "userinfo": {
    "email": "<user email>",
    "name": "<user name>",
    // ... other user info from Google
  },
  "token": "<Generated JWT>"
}
```
