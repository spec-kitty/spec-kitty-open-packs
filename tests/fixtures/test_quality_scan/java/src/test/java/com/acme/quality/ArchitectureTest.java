package com.acme.quality;

import org.junit.jupiter.api.Test;

class ArchitectureTest {
    @Test
    void onionDependsInward() {
        ONION_DOMAIN_DEPENDS_ON_NOTHING_OUTWARD.check(classes);
        ONION_APPLICATION_DEPENDS_ON_DOMAIN_ONLY.check(classes);
    }
}
