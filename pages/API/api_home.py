from typing import Dict, Any, Optional
import requests
from base.base_api_test import BaseApiTest
from pages.API.endpoints import EndPoints


class ApiHome:
    """
    API component library for common endpoints.
    Encapsulates API calls for reuse across tests.
    Uses EndPoints class for centralized endpoint management.
    """

    def __init__(self, apiTest: BaseApiTest) -> None:
        self.apiTest = apiTest
        self.endPoints = EndPoints()

    # Posts endpoints
    def getPosts(self) -> requests.Response:
        """Get all posts"""
        return self.apiTest.get(self.endPoints.POSTS)

    def getPostById(self, postId: int) -> requests.Response:
        """Get post by ID"""
        return self.apiTest.get(self.endPoints.getPostById(postId))

    def createPost(self, payload: Dict[str, Any]) -> requests.Response:
        """Create a new post"""
        return self.apiTest.post(self.endPoints.POSTS, json=payload)

    def updatePost(self, postId: int, payload: Dict[str, Any]) -> requests.Response:
        """Update an existing post"""
        return self.apiTest.put(self.endPoints.updatePost(postId), json=payload)

    def deletePost(self, postId: int) -> requests.Response:
        """Delete a post"""
        return self.apiTest.delete(self.endPoints.deletePost(postId))

    # Users endpoints
    def getUsers(self) -> requests.Response:
        """Get all users"""
        return self.apiTest.get(self.endPoints.USERS)

    def getUserById(self, userId: int) -> requests.Response:
        """Get user by ID"""
        return self.apiTest.get(self.endPoints.getUserById(userId))

