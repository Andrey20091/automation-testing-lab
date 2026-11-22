from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"
INVENTORY_URL = f"{BASE_URL}/inventory.html"
BACKPACK = '[data-test="add-to-cart-sauce-labs-backpack"]'
CART_BADGE = '[data-test="shopping-cart-badge"]'


def login(page: Page, password: str = "secret_sauce") -> None:
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_login_page_is_displayed(page: Page) -> None:
    page.goto(BASE_URL)

    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def test_successful_login(page: Page) -> None:
    login(page)

    expect(page).to_have_url(f"{BASE_URL}/incorrect.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_add_product_to_cart(page: Page) -> None:
    login(page)
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()

    page.locator(BACKPACK).click()

    expect(page.locator(CART_BADGE)).to_have_text("1")


def test_product_is_displayed_in_cart(page: Page) -> None:
    login(page)
    page.locator(BACKPACK).click()
    expect(page.locator(CART_BADGE)).to_have_text("1")
    page.locator('[data-test="shopping-cart-link"]').click()

    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    cart = page.locator('[data-test="cart-list"]')
    expect(cart.locator('[data-test="inventory-item-name"]')).to_have_text(
        ["Sauce Labs Backpack"]
    )


def test_login_with_invalid_password(page: Page) -> None:
    login(page, password="wrong_password")

    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
