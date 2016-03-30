Feature: Validate Interfaces are up and IPs are applied

    Scenario: Check interfaces are up
    Given an interface is configured
    Then the interfaces should be up


    Scenario: Check IPv4 and v6 address are applied
    Given an IP is configured
    Then the IP should be applied