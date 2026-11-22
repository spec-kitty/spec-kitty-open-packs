# Worked example: slicing a test by functional responsibility (user registration)

This example shows how to draw a test boundary around the behaviour under test instead of around a class or a layer. It follows the case study of Clear Test Boundaries (Stijn Dejongh, https://patterns.sddevelopment.be/practices/define_test_boundaries/). The code below is an illustrative reconstruction, not the source's own code, and the case is an analogy that supports the argument; it is not proof that every over-mocked test fails this way. Two heuristics at the end come from The Testing Pyramid (https://patterns.sddevelopment.be/concepts/testing_pyramid/).

## The behaviour

"A visitor registers with a valid email address and gets an account." Three collaborators deliver it:

- `UserRegistrationApi`: the entry point.
- `UserBusinessService`: the registration rules (duplicate check, account creation).
- `EmailValidationService`: the email-format rule the registration depends on.

The account is stored through `UserDatabaseProxy`, the persistence seam.

## Before: a test per layer

The team tested each layer in isolation. The API-level test substituted the business service, an internal collaborator in the same functional slice, and checked that a call was made:

```java
class UserRegistrationApiTest {
    UserBusinessService userService = mock(UserBusinessService.class);
    UserRegistrationApi api = new UserRegistrationApi(userService);

    @Test void registersUser() {
        api.register(new RegistrationRequest("ada@example.org", "s3cret!"));
        verify(userService, times(1)).createUser("ada@example.org", "s3cret!");
    }
}
```

The test proves that one method called another. It does not prove that registration works: if `createUser` rejected every address, this test would stay green.

Then the product added a Captcha step to registration. The API layer changed, and most API-level tests went red, because each one pinned the old calls between layers. They had to be updated with extra stubs, and the team's confidence dropped.

## After: one test for the functional slice

The boundary now encloses everything that co-delivers the behaviour. The business service and the email validation run for real. Only the database proxy is substituted, because persistence is an allow-listed seam (DIRECTIVE_054). The assertion targets the outcome.

```java
class UserRegistrationTest {
    InMemoryUserDatabase database = new InMemoryUserDatabase();   // substitute at the persistence seam
    UserRegistrationApi api = new UserRegistrationApi(
        new UserBusinessService(database, new EmailValidationService()));

    @Test void validEmailCreatesAccount() {
        RegistrationResponse response = api.register(new RegistrationRequest("ada@example.org", "s3cret!"));

        assertThat(response.status()).isEqualTo(RegistrationStatus.CREATED);
        assertThat(database.findByEmail("ada@example.org")).isPresent();
    }

    @Test void malformedEmailIsRejected() {
        RegistrationResponse response = api.register(new RegistrationRequest("not-an-email", "s3cret!"));

        assertThat(response.status()).isEqualTo(RegistrationStatus.INVALID_EMAIL);
        assertThat(database.count()).isZero();
    }
}
```

The in-memory database keeps the real dependency's contract: it can hold a user, refuse a duplicate and report absence, so no state appears that the real store could not produce.

Note on the Captcha step the product added: whether a test substitutes it depends on what sits behind it. A third-party Captcha service reached over the network is another system, so a substitute is allowed there; a Captcha rule the system owns runs for real. The example above leaves the Captcha step out.

## Boundary statement

"This test validates registration by exercising `UserRegistrationApi`, `UserBusinessService` and `EmailValidationService` for real, and substitutes only the user database."

## Checking the boundary

1. If the business service is split into two classes without changing behaviour, does the test still pass? Yes: it never named the internal call.
2. If the database implementation changes, is the test affected? No: the database sits outside the boundary.

## What the example teaches

- Identify the functionality under test, not the class under test.
- A well-scoped unit test needs few substitutes. Needing a double of owned logic means the boundary is drawn wrong: widen the slice or extract a pure seam.
- Write tests as if you were unaware of the internal structure: extracting a helper class should not change the suite.
- Boundaries drawn for today's design can fossilize: when the architecture moves, re-check them before trusting old substitutes.
- The cost is real: a wider slice takes more setup and the team must learn to draw boundaries. The payoff is a suite that survives refactoring.
