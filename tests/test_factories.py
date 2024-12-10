from tests.factories import ProductFactory

def test_product_factory():
    """Test that the ProductFactory generates valid products"""
    
    # Generate a product instance using the factory
    product = ProductFactory()

    # Validate the generated product's attributes
    assert product.name is not None, "Product name should not be None"
    assert isinstance(product.name, str), "Product name should be a string"

    assert product.price > 0, "Product price should be greater than 0"
    assert isinstance(product.price, float), "Product price should be a float"

    assert product.category in ["ELECTRONICS", "CLOTHING", "FOOD"], (
        f"Product category {product.category} is not valid"
    )
    assert isinstance(product.category, str), "Product category should be a string"

    assert isinstance(product.availability, bool), "Product availability should be a boolean"

