Feature: The product store service back-end
  As a Product Store Owner
  I need a RESTful catalog service
  So that I can keep track of all my products

  Background:
    Given the following products
      | name       | description     | price   | available | category   |
      | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
      | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
      | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
      | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

  Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Catalog Administration" in the title
    And I should not see "404 Not Found"

  Scenario: Read a Product
    Given the following products
      | name       | description     | price   | available | category   |
      | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
    When I set the "Id" field to "3"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Big Mac" in the "Name" field
    And I should see "1/4 lb burger" in the "Description" field
    And I should see "5.99" in the "Price" field

  Scenario: Update a Product
    Given the following products
      | name       | description     | price   | available | category   |
      | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
    When I set the "Id" field to "1"
    And I press the "Retrieve" button
    And I set the "Price" to "49.95"
    And I press the "Update" button
    Then I should see the message "Success"
    And I should see "49.95" in the "Price" field

  Scenario: Delete a Product
    Given the following products
      | name       | description     | price   | available | category   |
      | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
    When I set the "Id" field to "2"
    And I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Retrieve" button
    Then I should see the message "Not Found"

  Scenario: List All Products
    When I press the "List All" button
    Then I should see the following products
      | name       | description     | price   | available | category   |
      | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
      | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
      | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
      | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

  Scenario: Search Products by Category
    When I set the "Category" to "CLOTHS"
    And I press the "Search by Category" button
    Then I should see the following products
      | name       | description     | price   | available | category   |
      | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
      | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |

  Scenario: Search Products by Availability
    When I set the "Availability" to "True"
    And I press the "Search by Availability" button
    Then I should see the following products
      | name       | description     | price   | available | category   |
      | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
      | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
      | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

  Scenario: Search Products by Name
    When I set the "Name" to "Big Mac"
    And I press the "Search by Name" button
    Then I should see the following products
      | name       | description     | price   | available | category   |
      | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |

