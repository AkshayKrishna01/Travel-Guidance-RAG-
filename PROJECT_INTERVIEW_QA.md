# X Clone — Project Interview Questions and Answers

This guide is based on the current repository implementation. Answers distinguish implemented behavior from improvements that would be appropriate for a production system. Use the answers as prompts to explain your own decisions; do not claim that proposed improvements are already implemented.

## Project overview and architecture

### 1. What does this project do?

It is a full-stack social networking application modeled on core X interactions. Signed-in users can create text or image posts, browse a global feed or posts from followed users, like and comment on posts, follow accounts, view/edit profiles, and receive follow/like notifications.

### 2. What is the technology stack?

The client uses React 19, Vite, React Router, TanStack Query, Tailwind CSS 4, DaisyUI, and `react-hot-toast`. The API uses Node.js, Express 4, and Mongoose 6 over MongoDB. Authentication uses JWTs stored in HTTP-only cookies, passwords are hashed with bcrypt, and post images are uploaded to Cloudinary.

### 3. Describe the high-level architecture.

The Vite frontend sends credentialed HTTP requests to an Express REST API. Express route modules map URLs to controllers. Protected routes pass through JWT middleware, which loads the user and attaches it to `req.user`. Controllers validate the request, read/write Mongoose models, and return JSON. TanStack Query caches server responses and refetches affected data after mutations.

### 4. What happens when the application starts?

The frontend mounts React inside a query provider and browser router. `App` queries `/api/auth/me` to discover the current session and then conditionally renders authenticated routes and navigation. The backend loads environment variables, configures Cloudinary, middleware, CORS, and API routes, starts listening, and initiates a MongoDB connection.

### 5. How is the frontend organized?

`src/page` contains route-level screens; `src/components/common` contains shared navigation and post UI; `src/hooks` contains reusable mutations; and `src/utils` contains helpers such as date formatting. `App.jsx` owns route selection and the authenticated shell, while the pages compose feature-specific components.

## React and client-side state

### 6. What is TanStack Query used for?

It manages remote server state: fetching, caching, loading/error states, mutations, and invalidation. For example, login invalidates `authUser`, post creation invalidates `posts`, and profile updates invalidate both `authUser` and `userProfile`. This avoids manually synchronizing many copies of server data in component state.

### 7. How does the feed switch between “For you” and “Following”?

`HomePage` keeps a `feedType` value in local React state. `Posts` maps `forYou` to `/api/posts/all` and `following` to `/api/posts/following`, fetches with credentials, and renders loading skeletons, an empty message, or post cards.

### 8. How does the app handle loading and errors?

Queries expose loading/error state to screens. Feed and profile screens use skeletons or messages; mutations show toast feedback for success or failure. The implementation is not fully uniform: some query errors are displayed directly, while some components do not render a dedicated query error state.

### 9. How does image selection work on the client?

The browser `FileReader` converts a selected image into a base64 data URL. The component stores it in state and previews it. On submission, the frontend sends it in JSON; the post controller uploads it to Cloudinary and stores the returned secure URL.

### 10. Are post interactions optimistic?

No. Like, comment, delete, follow, and profile-update flows generally wait for the API response and invalidate related query keys. An optimistic approach could update the cache immediately and roll back on failure, but it requires careful handling of concurrent mutations and cache consistency.

### 11. How does client-side route protection work?

`App.jsx` checks the `authUser` query result and uses React Router `<Navigate>` to redirect unauthenticated users away from protected screens and authenticated users away from login/signup. This improves navigation and user experience, but actual authorization is enforced by backend middleware; a client route guard is not a security boundary.

## API and backend

### 12. How are API routes organized?

Routes are grouped by resource: `/api/auth`, `/api/users`, `/api/posts`, and `/api/notifications`. Each router declares HTTP methods and paths and delegates to controller functions. Protected endpoints include `protectRoute` in their middleware chain.

### 13. What does the authentication middleware do?

It reads `req.cookies.jwt`, verifies the token with `JWT_SECRET`, loads the matching user while excluding the password, sets `req.user`, and calls `next()`. Missing tokens produce an unauthorized response. The current generic catch returns 500 for token verification errors; returning 401 for invalid or expired tokens would be more accurate.

### 14. How does signup work?

The signup controller checks required fields, applies a basic email regex, checks for existing email/username, enforces a six-character minimum, hashes the password with bcrypt, saves a user, and generates a JWT cookie. It returns selected public account fields rather than the password hash.

### 15. How does login work?

The controller finds a user by username and compares the supplied password to the stored bcrypt hash. If credentials are valid, it issues a JWT cookie and returns account fields. It uses a generic invalid-credentials response so it does not reveal whether a username exists.

### 16. How is logout implemented?

The logout endpoint overwrites the `jwt` cookie with an empty value and a zero max age. The frontend then invalidates `authUser`, causing the app to recalculate the authenticated shell and route state.

### 17. How is password data protected?

Passwords are hashed using bcrypt before persistence, and authentication compares a candidate password with the stored hash. The JWT middleware also excludes the password field when it loads a request user. Public profile responses should use an explicit field projection as well; the current profile endpoint returns a full user document and therefore needs correction to avoid exposing the hash.

### 18. How are errors represented?

Controllers generally return a JSON object with an `error` message and an HTTP status. The frontend parses JSON and throws when `response.ok` is false, allowing TanStack Query mutation handlers to display the error. A centralized Express error handler and consistent validation/error shapes would make this easier to maintain.

## MongoDB and data modeling

### 19. What are the main data models?

There are three: `User`, `Post`, and `Notification`. Users store profile fields and relationship/liked-post ObjectId arrays. Posts reference an author and contain likes plus embedded comments. Notifications reference sender and recipient users and store a type and read flag. All three use timestamps.

### 20. Why are comments embedded in posts?

Embedding makes it straightforward to fetch a post with its comments and append a comment in one document operation. It is reasonable for a small prototype with bounded comment volume. If comments grow without bound or need independent moderation/search/pagination, a separate Comment collection would scale better.

### 21. Why are likes represented on both User and Post?

`Post.likes` supports rendering like counts and checking whether the current user liked a post. `User.likedPosts` supports listing posts liked by a particular user without scanning every post. This denormalization speeds those read patterns but requires both writes to remain consistent.

### 22. What are the risks of the current follow/like data model?

Follow relationships are stored in both users' `following` and `followers` arrays. Like state is stored in both the post and user. The controller performs separate writes, so a failure or simultaneous requests can leave the two sides inconsistent. MongoDB transactions or carefully designed atomic operations and reconciliation would improve correctness.

### 23. How does the following feed work?

The API loads the authenticated user's `following` array, queries posts where `user` is in that array, sorts by `createdAt` descending, and populates the author and comment authors. It currently returns every matching post in one response.

### 24. How would you scale feed reads?

I would add cursor-based pagination using `(createdAt, _id)` ordering, create indexes aligned with feed queries (for example, author plus creation time), limit populated fields, and measure query plans. At larger scale, I would evaluate a fan-out strategy or a dedicated feed store based on write/read patterns. The current implementation is a simple fan-in query and is suitable only while data volume is modest.

## Security and deployment

### 25. How are sessions stored in the browser?

The backend signs a JWT with a user ID and places it in an HTTP-only cookie. HTTP-only prevents client-side JavaScript from reading the token. The cookie is configured with `sameSite: "strict"`, and `secure` is enabled outside development. Cross-origin requests use `credentials: "include"` and the server permits credentials for its configured frontend origin.

### 26. What security improvements would you prioritize?

First, never serialize password hashes from profile endpoints; use explicit response DTOs/projections. Then validate and normalize all inputs, fix invalid-token status handling, add rate limits to authentication and write endpoints, limit/validate uploaded media, configure deployment CORS and HTTPS deliberately, and consider CSRF defenses appropriate to the cookie and deployment model. Secrets should be validated at startup and kept outside source control.

### 27. What is a notable authentication configuration bug?

The JWT expiry is 15 days, but the cookie `maxAge` expression is `15 * 24 * 60 * 1000`, which is 36 minutes in milliseconds. That means the browser cookie may expire long before the token does. The cookie max age should be calculated in milliseconds for the intended 15-day duration.

### 28. How are images stored?

The client sends a base64 data URL for a post image. The backend uploads it to Cloudinary and persists the secure URL, avoiding storage of image bytes directly in MongoDB. Post deletion attempts to remove the corresponding Cloudinary asset. Profile-image upload code exists but is commented out, so profile uploads currently do not follow the same completed upload flow.

### 29. How would you prepare this for production deployment?

I would configure the API origin from environment, set an explicit allowed frontend origin, require HTTPS and secure cookies, validate all required secrets and service credentials at startup, serve the built frontend from a static host or configure Express static/fallback handling, add health checks and graceful shutdown, and run migrations/data checks as needed. The current server has no static frontend serving and has local development origins hard-coded.

## Feature behavior and tradeoffs

### 30. How does a like operation work?

The controller loads the post and checks if the authenticated user ID is already in `post.likes`. If yes, it removes the ID from the post and the user's `likedPosts`; otherwise it adds it to both and creates a like notification. The response contains the updated likes array. This is a toggle endpoint, so repeated requests alternate state.

### 31. How does following work?

The route rejects self-following, checks that both users exist, and tests whether the target is already in the current user's `following` list. It pulls the reciprocal IDs to unfollow or pushes both IDs to follow; on follow it creates a notification. The two user writes are not atomic as a unit.

### 32. What does reading notifications do?

`GET /api/notifications` queries notifications addressed to the authenticated user, populates sender data, marks all of that user's notifications as read, and returns the list. `DELETE` removes all notifications for that user. The current response is not explicitly sorted.

### 33. Which visible controls are not functional yet?

The repost and bookmark icons in the post card are presentation-only. The emoji icon in the create-post form does not open a picker. There is no repost/bookmark model or endpoint in the backend.

## Testing, maintenance, and reflection

### 34. How would you test this project?

I would unit-test validation and controller behavior, integration-test Express routes against a disposable MongoDB instance, and test key UI flows such as signup/login, creating a post, liking/unliking, following/unfollowing, and authorization failures. I would also add tests for password non-disclosure and relationship consistency. The repository currently does not define a working automated test suite.

### 35. What was a challenging engineering problem in the project?

A good discussion point is maintaining coherence across client cache, API state, and MongoDB relationships. For example, a follow action affects the current user's following list, the target user's follower list, suggested-user results, and potentially notifications. TanStack Query invalidation refreshes the client view, while backend consistency still depends on keeping both database relationship arrays synchronized.

### 36. What would you improve first if you had more time?

I would fix user-data exposure by returning explicit public projections, correct the JWT cookie lifetime, improve request validation and error handling, and make relationship updates atomic. Next I would add pagination and database indexes, complete a consistent image upload pipeline, configure deployment origins, and establish API and UI test coverage.

### 37. What did you learn from the project?

It demonstrates how a React client, a REST API, cookie-based auth, database models, cloud media storage, and query caching fit together. It also makes the tradeoffs visible: denormalized data can speed reads but adds consistency work, cookie auth requires careful CORS/browser configuration, and a working prototype still needs validation, tests, pagination, and deployment hardening.

## Rapid revision checklist

- **Auth:** bcrypt hash, JWT with user ID, HTTP-only cookie, middleware loads `req.user`.
- **Client server state:** TanStack Query; mutations invalidate query keys.
- **Database:** MongoDB/Mongoose; referenced users, embedded post comments, denormalized likes/follows.
- **Media:** base64 browser payload → Cloudinary upload → secure URL on post.
- **Known correctness issue:** 15-day JWT but 36-minute cookie max age.
- **Known security issue:** profile route currently returns the full user document, including password hash.
- **Known scalability issue:** feeds return all results without pagination.
- **Known incomplete features:** repost, bookmark, emoji picker, profile image Cloudinary upload.
