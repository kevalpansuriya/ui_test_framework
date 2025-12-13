from typing import Dict, Any
import requests
from base.base_api_test import BaseApiTest


class EndPoints:
    """
    Centralized endpoint definitions for API tests
    All endpoints are stored here for easy maintenance
    """
    
    # Posts endpoints
    GET_POSTS = "/posts"
    GET_POST_BY_ID = "/posts/{postId}"
    POST_CREATE_POST = "/posts"
    PUT_UPDATE_POST = "/posts/{postId}"
    DELETE_POST = "/posts/{postId}"
    
    # Users endpoints
    GET_USERS = "/users"
    GET_USER_BY_ID = "/users/{userId}"

class ApiHome:
    """
    API component library for common endpoints.
    Encapsulates API calls and validation logic for reuse across tests.
    Uses EndPoints class for centralized endpoint management.
    """

    def __init__(self, apiTest: BaseApiTest) -> None:
        self.apiTest = apiTest
        self.logger = apiTest.logger
        self.endPoints = EndPoints()

    # Posts endpoints
    def getPosts(self) -> requests.Response:
        """Get all posts"""
        return self.apiTest.get(self.endPoints.GET_POSTS)

    def getPostById(self, postId: int) -> requests.Response:
        """Get post by ID"""
        return self.apiTest.get(self.endPoints.GET_POST_BY_ID.format(postId=postId))

    def createPost(self, payload: Dict[str, Any]) -> requests.Response:
        """Create a new post"""
        return self.apiTest.post(self.endPoints.POST_CREATE_POST, json=payload)

    def updatePost(self, postId: int, payload: Dict[str, Any]) -> requests.Response:
        """Update an existing post"""
        return self.apiTest.put(self.endPoints.PUT_UPDATE_POST.format(postId=postId), json=payload)

    def deletePost(self, postId: int) -> requests.Response:
        """Delete a post"""
        return self.apiTest.delete(self.endPoints.DELETE_POST.format(postId=postId))

    # Users endpoints
    def getUsers(self) -> requests.Response:
        """Get all users"""
        return self.apiTest.get(self.endPoints.GET_USERS)

    def getUserById(self, userId: int) -> requests.Response:
        """Get user by ID"""
        return self.apiTest.get(self.endPoints.GET_USER_BY_ID.format(userId=userId))

    # Validation methods
    def _validateResponse(self, response: requests.Response, expectedStatusCode: int) -> Any:
        """
        Common validation method to check status code and return JSON response
        
        Args:
            response: Response object from API call
            expectedStatusCode: Expected HTTP status code
            
        Returns:
            JSON data from response
        """
        self.apiTest.assertStatusCode(response, expectedStatusCode)
        return response.json()
    
    def verifyGetAllUsers(self, response: requests.Response) -> None:
        """
        Verify GET all users response
        
        Args:
            response: Response object from getUsers call
        """
        users = self._validateResponse(response, 200)
        assert isinstance(users, list), "Response should be a list"
        assert len(users) > 0, "Users list should not be empty"
        self.logger.info(f"Successfully retrieved {len(users)} users")
    
    def verifyGetUserById(self, response: requests.Response, userId: int) -> None:
        """
        Verify GET user by ID response
        
        Args:
            response: Response object from getUserById call
            userId: Expected user ID
        """
        user = self._validateResponse(response, 200)
        assert user["id"] == userId, f"User ID should be {userId}"
        self.apiTest.assertResponseContains(response, "name")
        self.apiTest.assertResponseContains(response, "email")
        self.apiTest.assertResponseContains(response, "address")
        self.logger.info(f"Successfully retrieved user with ID: {userId}")
    
    def verifyGetAllPosts(self, response: requests.Response) -> None:
        """
        Verify GET all posts response
        
        Args:
            response: Response object from getPosts call
        """
        posts = self._validateResponse(response, 200)
        assert isinstance(posts, list), "Response should be a list"
        assert len(posts) > 0, "Posts list should not be empty"
        self.logger.info(f"Successfully retrieved {len(posts)} posts")
    
    def verifyGetPostById(self, response: requests.Response, postId: int) -> None:
        """
        Verify GET post by ID response
        
        Args:
            response: Response object from getPostById call
            postId: Expected post ID
        """
        post = self._validateResponse(response, 200)
        assert post["id"] == postId, f"Post ID should be {postId}"
        self.apiTest.assertResponseContains(response, "title")
        self.apiTest.assertResponseContains(response, "body")
        self.apiTest.assertResponseContains(response, "userId")
        self.logger.info(f"Successfully retrieved post with ID: {postId}")
    
    def verifyCreatePost(self, response: requests.Response, expectedPost: Dict[str, Any]) -> None:
        """
        Verify POST create post response
        
        Args:
            response: Response object from createPost call
            expectedPost: Expected post data
        """
        createdPost = self._validateResponse(response, 201)
        assert createdPost["title"] == expectedPost["title"], "Title should match"
        assert createdPost["body"] == expectedPost["body"], "Body should match"
        assert "id" in createdPost, "Created post should have an ID"
        self.logger.info(f"Successfully created post with ID: {createdPost.get('id')}")
    
    def verifyUpdatePost(self, response: requests.Response, expectedPost: Dict[str, Any]) -> None:
        """
        Verify PUT update post response
        
        Args:
            response: Response object from updatePost call
            expectedPost: Expected post data
        """
        post = self._validateResponse(response, 200)
        assert post["title"] == expectedPost["title"], "Title should be updated"
        assert post["body"] == expectedPost["body"], "Body should be updated"
        self.logger.info(f"Successfully updated post with ID: {expectedPost.get('id')}")
    
    def verifyDeletePost(self, response: requests.Response, postId: int) -> None:
        """
        Verify DELETE post response
        
        Args:
            response: Response object from deletePost call
            postId: Deleted post ID
        """
        self.apiTest.assertStatusCode(response, 200)
        self.logger.info(f"Successfully deleted post with ID: {postId}")

