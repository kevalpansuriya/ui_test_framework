"""
EndPoints class - Centralized endpoint definitions
Following SRP - handles only endpoint URL management
"""


class EndPoints:
    """
    Centralized endpoint definitions for API tests
    All endpoints are stored here for easy maintenance
    """
    
    # Posts endpoints
    POSTS = "/posts"
    POST_BY_ID = "/posts/{id}"
    
    # Users endpoints
    USERS = "/users"
    USER_BY_ID = "/users/{id}"
    
    @staticmethod
    def getPostById(postId: int) -> str:
        """Get post by ID endpoint"""
        return f"/posts/{postId}"
    
    @staticmethod
    def getUserById(userId: int) -> str:
        """Get user by ID endpoint"""
        return f"/users/{userId}"
    
    @staticmethod
    def updatePost(postId: int) -> str:
        """Update post endpoint"""
        return f"/posts/{postId}"
    
    @staticmethod
    def deletePost(postId: int) -> str:
        """Delete post endpoint"""
        return f"/posts/{postId}"

