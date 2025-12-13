import pytest
from base.base_api_test import BaseApiTest
from pages.API.posts_api import PostsApi


@pytest.mark.api
class TestPostsApi(BaseApiTest):
    """
    API tests for Posts endpoint following SRP and camelCase naming
    """
    
    def setup_method(self):
        """Setup method called before each test"""
        self._initialize()
        self.postsApi = PostsApi(self)
        self.logger.info("Setting up Posts API test")
    
    @pytest.mark.smoke
    def testGetAllPosts(self):
        """
        Test GET all posts
        
        Test Steps:
        1. Send a GET request to retrieve all posts from the API
        2. Verify that the response status code is 200 (success)
        3. Verify that the response contains a list of posts
        4. Verify that the list is not empty
        5. Log the number of posts retrieved
        """
        response = self.postsApi.getPosts()
        self.postsApi.verifyGetAllPosts(response)
    
    @pytest.mark.regression
    def testGetPostById(self):
        """
        Test GET post by ID
        
        Test Steps:
        1. Set the post ID to 1
        2. Send a GET request to retrieve the post with the specified ID
        3. Verify that the response status code is 200 (success)
        4. Verify that the returned post has the correct ID
        5. Verify that the post contains required fields: title, body, and userId
        6. Log that the post was successfully retrieved
        """
        postId = 1
        response = self.postsApi.getPostById(postId)
        self.postsApi.verifyGetPostById(response, postId)
    
    @pytest.mark.regression
    def testCreatePost(self):
        """
        Test POST create new post
        
        Test Steps:
        1. Create a new post object with title, body, and userId
        2. Send a POST request to create the new post
        3. Verify that the response status code is 201 (created)
        4. Verify that the created post has the same title as the input
        5. Verify that the created post has the same body as the input
        6. Verify that the created post has been assigned an ID
        7. Log the ID of the newly created post
        """
        newPost = {
            "title": "Test Post Title",
            "body": "Test Post Body",
            "userId": 1
        }
        response = self.postsApi.createPost(newPost)
        self.postsApi.verifyCreatePost(response, newPost)
    
    @pytest.mark.regression
    def testUpdatePost(self):
        """
        Test PUT update post
        
        Test Steps:
        1. Set the post ID to 1 (the post to be updated)
        2. Create an updated post object with new title and body
        3. Send a PUT request to update the post with the new data
        4. Verify that the response status code is 200 (success)
        5. Verify that the updated post has the new title
        6. Verify that the updated post has the new body
        7. Log that the post was successfully updated
        """
        postId = 1
        updatedPost = {
            "id": postId,
            "title": "Updated Test Post Title",
            "body": "Updated Test Post Body",
            "userId": 1
        }
        response = self.postsApi.updatePost(postId, updatedPost)
        self.postsApi.verifyUpdatePost(response, updatedPost)
    
    @pytest.mark.regression
    def testDeletePost(self):
        """
        Test DELETE post
        
        Test Steps:
        1. Set the post ID to 1 (the post to be deleted)
        2. Send a DELETE request to remove the post
        3. Verify that the response status code is 200 (success)
        4. Log that the post was successfully deleted
        """
        postId = 1
        response = self.postsApi.deletePost(postId)
        self.postsApi.verifyDeletePost(response, postId)
    
    @pytest.mark.regression
    def testGetPostWithInvalidId(self):
        """
        Test that intentionally fails to demonstrate error handling for invalid post ID
        
        Test Steps:
        1. Set an invalid post ID (999999 - a very large number that doesn't exist)
        2. Send a GET request to retrieve the post with the invalid ID
        3. This test expects a 200 status code but will fail because the post doesn't exist
        4. The test will show detailed error information in the test report
        5. This demonstrates how API test failures are reported with full error details
        """
        invalidPostId = 999999
        response = self.postsApi.getPostById(invalidPostId)
        
        # This will fail because the post with ID 999999 doesn't exist
        # The verification will fail and show detailed error information
        self.postsApi.verifyGetPostById(response, invalidPostId)

