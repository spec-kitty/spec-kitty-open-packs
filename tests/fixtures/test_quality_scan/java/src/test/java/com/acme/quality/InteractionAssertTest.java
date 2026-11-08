package com.acme.quality;

import org.junit.jupiter.api.Test;
import org.mockito.InOrder;

import static org.mockito.Mockito.inOrder;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;

class InteractionAssertTest {
    @Test
    void verifiesACollaboratorCall() {
        verify(mock).run();
    }

    @Test
    void verifiesNoCollaboratorCalls() {
        verifyNoInteractions(mock);
    }

    @Test
    void verifiesCollaboratorOrder() {
        InOrder order = inOrder(mock);
        order.verify(mock).run();
    }
}
