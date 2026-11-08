package com.acme.quality;

class Ignored {
    @org.junit.jupiter.api.Test
    void notDiscoveredBecauseTheFileNameDoesNotMatch() {
        service.run();
    }
}
