from pages.login_page import LoginPage

def test_valid_login(page, config, logger):
    logger.info("Starting valid login test")
    login_page = LoginPage(page)
    login_page.visit("https://example.com/login")
    login_page.login(config["valid_user"]["username"], config["valid_user"]["password"])
    assert "Dashboard" in login_page.get_title(), "Login failed!"
    logger.info("Valid login test completed successfully")

def test_invalid_login(page, config, logger):
    logger.info("Starting invalid login test")
    login_page = LoginPage(page)
    login_page.visit("https://example.com/login")
    login_page.login(config["invalid_user"]["username"], config["invalid_user"]["password"])
    assert "Login Failed" in login_page.get_title(), "Error handling failed!"
    logger.info("Invalid login test completed successfully")