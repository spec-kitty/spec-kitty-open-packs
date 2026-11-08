package com.acme.quality;

import com.tngtech.archunit.lang.ArchRule;
import org.junit.jupiter.api.Test;

class ArchitectureTest {
    private ArchRule ONION_DOMAIN_DEPENDS_ON_NOTHING_OUTWARD;
    private ArchRule ONION_APPLICATION_DEPENDS_ON_DOMAIN_ONLY;
    @Test
    void onionDependsInward() {
        ONION_DOMAIN_DEPENDS_ON_NOTHING_OUTWARD.check(classes);
        ONION_APPLICATION_DEPENDS_ON_DOMAIN_ONLY.check(classes);
    }
}
