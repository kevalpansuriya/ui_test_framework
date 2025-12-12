"""
Validation components for API responses
Following SRP - handles only validation logic
"""
from typing import Dict, Any, List
import requests
from base.base_api_test import BaseApiTest


class ApiValidations:
    """
    Validation components for API responses
    Encapsulates common validation logic for reuse across tests
    """
    
    def __init__(self, apiTest: BaseApiTest) -> None:
        self.apiTest = apiTest
        self.logger = apiTest.logger
    
    def verifyGetAllUsers(self, response: requests.Response) -> None:
        """
        Verify GET all users response
        
        Args:
            response: Response object from getUsers call
        """
        self.apiTest.assertStatusCode(response, 200)
        users = response.json()
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
        self.apiTest.assertStatusCode(response, 200)
        user = response.json()
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
        self.apiTest.assertStatusCode(response, 200)
        posts = response.json()
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
        self.apiTest.assertStatusCode(response, 200)
        post = response.json()
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
        self.apiTest.assertStatusCode(response, 201)
        createdPost = response.json()
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
        self.apiTest.assertStatusCode(response, 200)
        post = response.json()
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

