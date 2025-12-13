import pytest
from base.base_api_test import BaseApiTest
from pages.API.api_home import ApiHome


@pytest.mark.api
class TestPostsApi(BaseApiTest):
    """
    API tests for Posts endpoint following SRP and camelCase naming
    """
    
    def setup_method(self):
        """Setup method called before each test"""
        self._initialize()
        self.apiHome = ApiHome(self)
        self.logger.info("Setting up Posts API test")
    
    @pytest.mark.smoke
    def testGetAllPosts(self):
        """Test GET all posts"""
        response = self.apiHome.getPosts()
        self.apiHome.verifyGetAllPosts(response)
    
    @pytest.mark.regression
    def testGetPostById(self):
        """Test GET post by ID"""
        postId = 1
        response = self.apiHome.getPostById(postId)
        self.apiHome.verifyGetPostById(response, postId)
    
    @pytest.mark.regression
    def testCreatePost(self):
        """Test POST create new post"""
        newPost = {
            "title": "Test Post Title",
            "body": "Test Post Body",
            "userId": 1
        }
        response = self.apiHome.createPost(newPost)
        self.apiHome.verifyCreatePost(response, newPost)
    
    @pytest.mark.regression
    def testUpdatePost(self):
        """Test PUT update post"""
        postId = 1
        updatedPost = {
            "id": postId,
            "title": "Updated Test Post Title",
            "body": "Updated Test Post Body",
            "userId": 1
        }
        response = self.apiHome.updatePost(postId, updatedPost)
        self.apiHome.verifyUpdatePost(response, updatedPost)
    
    @pytest.mark.regression
    def testDeletePost(self):
        """Test DELETE post"""
        postId = 1
        response = self.apiHome.deletePost(postId)
        self.apiHome.verifyDeletePost(response, postId)

