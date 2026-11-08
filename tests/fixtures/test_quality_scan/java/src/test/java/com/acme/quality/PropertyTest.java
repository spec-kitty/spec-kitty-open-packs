package com.acme.quality;

import net.jqwik.api.Property;

class PropertyTest {
    @Property
    void jqwikPropertiesAreNotJUnitTests() {
        service.run();
    }
}
