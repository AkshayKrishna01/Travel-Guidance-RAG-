# X Clone — Technical Project Documentation

## 1. Project overview

This repository contains a single-page social networking application modeled on the core interaction patterns of X. Authenticated users can create text and image posts, browse a global or following feed, like and comment on posts, follow other accounts, edit selected profile fields, and receive follow/like notifications.

The application is split into two deployable parts:

- **Frontend:** React 19, React Router, TanStack Query, Vite, Tailwind CSS 4, DaisyUI, and `react-hot-toast`.
- **Backend:** Node.js with Express 4, MongoDB through Mongoose 6, JWT cookie authentication, bcrypt password hashing, and optional Cloudinary image uploads.

The app is a functional prototype rather than a production-ready social network. There is no automated test suite, no pagination, no real-time transport, and several feature controls are visual placeholders. Details and observed implementation caveats are documented below.

## 2. Repository layout

```text
.
├── package.json                 # Root development/build/start scripts
├── backend/
│   ├── server.js                # Express setup, middleware, routes, startup
│   ├── db/connectDB.js          # Mongoose connection
│   ├── models/                  # User, Post, Notification schemas
│   ├── routes/                  # HTTP route declarations
│   ├── controller/              # Request handling and persistence logic
│   ├── middleware/protectRoute.js
│   └── utils/generateToken.js   # JWT creation and cookie configuration
└── frontend/
    ├── src/main.jsx             # React root, router, query client
    ├── src/App.jsx              # Auth bootstrap, route guards, app shell
    ├── src/page/                 # Home, profile, auth, notification screens
    ├── src/components/           # Shared UI, posts, navigation, skeletons
    ├── src/hooks/                # Follow and profile update mutations
    ├── src/constant/url.jsx      # API origin constant
    └── src/utils/                # Date formatting and sample data
```

The frontend is an ES module Vite application. The backend is also configured as an ES module (`"type": "module"`). The root package coordinates commands but is not itself the server or client application.

## 3. Runtime architecture

### Request and rendering flow

1. `frontend/src/main.jsx` mounts React under `React.StrictMode`, a shared TanStack `QueryClientProvider`, and `BrowserRouter`.
2. `App.jsx` runs `GET /api/auth/me` with `credentials: "include"`. The returned user is cached under `authUser` and controls route access and whether the authenticated sidebar/right panel are rendered.
3. Page components issue JSON `fetch` requests to the backend at the constant origin `http://localhost:5000` in `src/constant/url.jsx`.
4. Mutations use TanStack Query. On success, relevant cached queries are invalidated so pages refetch server state. Toasts communicate many mutation outcomes.
5. Express parses JSON and URL-encoded request bodies (up to 20 MB), parses cookies, applies CORS, mounts route modules, then connects to MongoDB when the HTTP server starts.
6. Protected routes verify the `jwt` cookie, load the corresponding user (excluding the password), assign it to `req.user`, and pass control to the controller.

### Backend middleware and service integrations

- CORS is currently configured for exactly `http://localhost:5173` and allows credentialed requests.
- `cookie-parser` exposes `req.cookies` for JWT authentication.
- `express.json` and `express.urlencoded` have a 20 MB limit, accommodating base64 image payloads at the cost of larger request bodies.
- Cloudinary is configured from environment variables in `backend/server.js`. Post creation attempts to upload an image and stores the resulting secure URL. Profile image upload code is present but commented out.
- MongoDB connection uses `process.env.MONGO_URL`; a connection failure logs and exits the process.

## 4. Data model

All schemas use Mongoose timestamps, so persisted documents receive `createdAt` and `updatedAt`.

### User (`backend/models/user.model.js`)

| Field | Type / behavior | Purpose |
|---|---|---|
| `userName` | String, required, unique | Account handle and profile route key |
| `fullName` | String, required | Display name |
| `email` | String, required, unique | Account email |
| `password` | String, required, minimum 6 chars | bcrypt hash after registration or password change |
| `followers` | Array of User ObjectIds | Accounts following this user |
| `following` | Array of User ObjectIds | Accounts this user follows |
| `profileImg`, `coverImg` | String, default empty | Image URL/data as stored by profile logic |
| `bio`, `link` | String, default empty | Profile metadata |
| `likedPosts` | Array of Post ObjectIds | Reverse index used to load a user's liked posts |

There are no schema-level email format rules or username normalization rules. Signup performs its own email-format and duplicate checks in the controller. Password hashing is performed in the auth and profile-update controllers rather than schema middleware.

### Post (`backend/models/post.model.js`)

| Field | Type / behavior | Purpose |
|---|---|---|
| `user` | Required User ObjectId reference | Author |
| `text` | String | Post text; optional if an image is supplied |
| `img` | String | Image URL after upload (or optional image reference) |
| `likes` | User ObjectId array | Accounts that liked the post |
| `comments` | Embedded array of `{ text, user }` | Comment text and author reference |

Comments are embedded in the post document, while users are referenced. Like membership is represented both in `Post.likes` and `User.likedPosts`; the like controller updates both collections.

### Notification (`backend/models/notification.model.js`)

`from` and `to` are required User references. `type` is restricted to `follow` or `like`; `read` defaults to false. Notifications are generated on follow and like events. A GET of a user's notifications marks all of that user's notifications read.

## 5. HTTP API

All paths below are mounted under `/api`. Unless stated otherwise, the route requires a valid `jwt` cookie and responds with JSON. Error responses generally use `{ "error": "..." }`.

### Authentication — `/api/auth`

| Method | Path | Auth | Behavior |
|---|---|---:|---|
| `POST` | `/signup` | No | Validates required fields, basic email syntax, uniqueness and password length; hashes password; creates user; sets JWT cookie; returns public user fields. |
| `POST` | `/login` | No | Looks up by username, compares bcrypt hash, sets JWT cookie and returns public user fields. |
| `POST` | `/logout` | No | Sets the JWT cookie to an empty value with zero max age. |
| `GET` | `/me` | Yes | Returns current user with password excluded. |

### Users — `/api/users`

| Method | Path | Auth | Behavior |
|---|---|---:|---|
| `GET` | `/profile/:userName` | Yes | Returns a user document matching the handle. |
| `POST` | `/follow/:id` | Yes | Toggles follow state; updates follower/following arrays and creates a follow notification when following. |
| `GET` | `/suggested` | Yes | Samples up to ten other users, removes followed users, and returns up to four suggestions. |
| `POST` | `/update` | Yes | Updates profile fields and optionally changes password after current-password verification. |

### Posts — `/api/posts`

| Method | Path | Auth | Behavior |
|---|---|---:|---|
| `GET` | `/all` | Yes | Returns all posts newest first, with author and comment authors populated. |
| `GET` | `/following` | Yes | Returns posts by accounts in the current user's following list, newest first. |
| `GET` | `/user/:userName` | Yes | Returns posts authored by the named user, newest first. |
| `GET` | `/likes/:id` | Yes | Finds a user and returns posts whose IDs occur in that user's `likedPosts`. |
| `POST` | `/create` | Yes | Requires text or image; uploads image to Cloudinary when present; saves a post. |
| `POST` | `/like/:id` | Yes | Toggles a like, synchronizes the user's liked-post list, and creates a like notification when adding a like. |
| `POST` | `/comment/:id` | Yes | Adds a non-empty text comment with the current user's reference. |
| `DELETE` | `/:id` | Yes | Deletes a post only if the current user owns it; also attempts to delete its Cloudinary image. |

### Notifications — `/api/notifications`

| Method | Path | Auth | Behavior |
|---|---|---:|---|
| `GET` | `/` | Yes | Returns notifications addressed to the current user and marks them read. |
| `DELETE` | `/` | Yes | Deletes all notifications addressed to the current user. |

## 6. Frontend features and component responsibilities

### App shell and routing

`App.jsx` defines `/`, `/login`, `/signup`, `/notifications`, and `/profile/:userName`. Home, notification, and profile screens redirect unauthenticated users to login; login and signup redirect authenticated users home. The shell conditionally shows `Sidebar` and `RightPanel`. `Toaster` provides global toast display.

### Home and feed

`HomePage` keeps local `feedType` state (`forYou` or `following`) and renders the create-post form and `Posts`. `Posts` maps feed types to API endpoints, uses a query key beginning with `posts`, displays loading skeletons and empty states, and renders each item through `Post`.

`CreatePost` loads `authUser`, converts a selected image file to a base64 data URL with `FileReader`, previews/removes the image, and submits `{ text, img }`. Success clears the form and invalidates the posts query.

`Post` renders author metadata, text/image, comments, likes, and owner-only deletion. Comments use a native HTML `<dialog>` modal. Like, comment, and delete actions are mutations that invalidate the `posts` cache. Repost and bookmark controls are currently presentation-only; emoji selection is also not implemented.

### Profile

`ProfilePage` loads the logged-in user and profile user independently, then presents profile metadata, follower counts, a follow toggle, edit form, and posts/likes tabs. The edit modal supports name, email, bio, link, and password changes. Profile and cover image selection is previewed in the page and sent through the profile-update mutation, although backend Cloudinary upload handling for these image fields is commented out.

### Notifications

`NotificationPage` loads notifications and offers a delete-all mutation. It renders an icon and text based on the notification type. The backend population selects `username` while the User schema uses `userName`, and the page also reads `notification.from.username`; this mismatch can leave the displayed handle undefined.

### Navigation and suggestions

`Sidebar` provides Home, Notifications, Profile, and logout actions. `RightPanel` requests suggested users and invokes the shared follow mutation. Responsive utility classes hide portions of the navigation/panel at smaller widths.

### Shared helpers and design system

`formatPostDate` produces relative minute/hour/day labels and a month/day label for older posts. `formatMemberSinceDate` formats a join month/year. Skeleton components represent loading states. Tailwind/DaisyUI classes define layout and theme; the selected DaisyUI black theme overrides primary and secondary colors.

## 7. Client-side data and mutation behavior

TanStack Query is the server-state cache. The root client disables refetch-on-window-focus. Common keys include `authUser`, `posts`, `userProfile`, `suggestedUsers`, and `notifications`. Mutations usually invalidate keys after success rather than applying optimistic updates.

The profile hook posts the complete form object to `/api/users/update` and invalidates both auth and profile queries. The follow hook posts to `/api/users/follow/:id` and invalidates suggestions and auth state. Login/signup invalidate `authUser`; logout invalidates it to force route reevaluation.

Because profile posts and likes share a broad `posts` key with feed queries and profile query keys do not include the feed type, cache invalidation and refetch behavior should be reviewed when changing these screens. There is no pagination or infinite-scroll abstraction; feed endpoints return full result sets.

## 8. Authentication and security model

Passwords are hashed using bcrypt with a generated salt (10 rounds in current controller code). The server signs JWTs containing `userId`, with a 15-day expiry. The token is written to an HTTP-only cookie with `sameSite: "strict"`; `secure` is enabled whenever `NODE_ENV` is not `development`. Protected endpoints verify the JWT and attach a password-excluded user to the request.

The browser must send credentials (`credentials: "include"`) for cookie-backed API access. The configured CORS origin must exactly match the frontend origin. The current configuration is local-development oriented, and the hard-coded API URL/CORS origin need environment/deployment configuration for non-local hosting.

## 9. Environment configuration and running locally

The backend reads a `.env` file using `dotenv` and expects:

| Variable | Used for |
|---|---|
| `PORT` | Express listen port; defaults to 5000 |
| `MONGO_URL` | MongoDB connection string |
| `JWT_SECRET` | JWT signing and verification secret |
| `NODE_ENV` | Cookie secure flag and environment behavior |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary account name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret read by server configuration |

Do not commit real credentials. The checked-in environment files should be treated as configuration artifacts and reviewed/rotated if they contain live secrets. The frontend currently does not read a Vite environment variable for the API URL; it uses `http://localhost:5000` in source.

Typical local startup is:

1. Configure backend environment values and ensure MongoDB and Cloudinary are available (Cloudinary is needed for image post uploads).
2. Install root and frontend dependencies using the package manifests/lockfiles.
3. Start the API with the root development script or from `backend` with its start script.
4. Start Vite from `frontend` with `npm run dev`; its configured development origin is normally `http://localhost:5173`.

The root `dev` script uses `NODE_ENV=development nodemon ...`, which is shell syntax that may not work in Windows PowerShell/cmd without a cross-platform wrapper. `cross-env` is present in dependencies and used by the root production start script, but not by that `dev` script. The root `build` script installs dependencies and builds the frontend; root `start` builds the frontend and runs the backend in production mode. The Express server shown here does not define static-file serving for the generated frontend, so production hosting needs a separate static frontend host or an additional Express static/fallback configuration.

## 10. Implementation observations and known limitations

These are observations from the current source, useful for maintainers; they are not claims that the app has been executed or tested.

1. **User privacy:** `GET /api/users/profile/:userName` returns the full Mongoose user document, including the password hash, rather than selecting public fields. This endpoint is authenticated, but the hash should still never be returned. The suggested-user endpoint separately nulls the password after aggregation, and that approach should also be replaced with an explicit projection.
2. **Cookie lifetime mismatch:** `generateToken` sets `maxAge` to `15*24*60*1000` milliseconds (36 minutes), while the JWT expiry is 15 days. The cookie can expire much earlier than the token.
3. **JWT error status:** `protectRoute` catches token verification errors in a generic catch and returns 500. Missing cookies return 401, but invalid/expired tokens should normally be treated as unauthenticated (401).
4. **Environment key consistency:** `server.js` reads `CLOUDINARY_API_SECRET`; the checked-in env key names should be checked to ensure this exact key exists. Configuration files also list a `CLOUDINARY_API_SECRET_KEY` name, which the server does not read.
5. **Signup browser credentials:** Signup's fetch does not set `credentials: "include"`, despite the backend setting a cookie. The signup controller creates the cookie, but subsequent auth bootstrap depends on the browser retaining/sending it under the configured CORS rules.
6. **Profile validation and uniqueness:** Profile updates accept email/username fields without checking uniqueness or validating email. Duplicate values may cause a MongoDB unique-index error and the controller returns a generic 500.
7. **Empty profile values:** Updates use `value || existingValue`, so fields cannot be intentionally cleared to an empty string.
8. **Image lifecycle:** Post images are uploaded to Cloudinary and deletion derives a public ID by splitting the URL. Profile-image upload code is commented out, and the frontend still submits those image fields. The body limit permits large base64 uploads without explicit MIME, size, or dimension validation.
9. **Relationship consistency and concurrency:** Follow state updates two user documents in separate writes. Likes update the post and user in separate writes. Failures or concurrent requests can leave these denormalized arrays inconsistent; transactions or atomic update patterns would improve reliability.
10. **Self-notifications:** The like route creates a notification even when a user likes their own post. Follow notifications are only created on follow, not unfollow.
11. **Notification references:** The notification population/page use `username`; the schema field is `userName`. The notification response also has no explicit sort, so ordering is unspecified.
12. **Post display routes:** A post handle link is built as `/profile/:${postOwner.userName}`, including a colon in the URL. Profile routes expect `/profile/<userName>`.
13. **Counts and sample data:** The profile header displays `POSTS.length` from local dummy data rather than the fetched user's post count. Dummy posts/users remain in `src/utils/db/dummy.js`, although primary feeds use the API.
14. **Pagination and scalability:** Global feed and other post queries return all matching records and populate referenced data. There are no indexes declared beyond unique user fields and no pagination, filtering, or rate limiting in the shown code.
15. **Operational behavior:** The server starts listening before `connectMongoDB()` resolves. It may accept requests before the DB is ready. There is no graceful shutdown or centralized request logging/error middleware.
16. **Project metadata:** The frontend HTML still has a Vite/React title and Vite favicon. The README is the unmodified Vite template. The backend package's test script explicitly reports that no tests are specified.

## 11. Suggested technical evolution

For a maintainable next iteration, prioritize: explicit public-field projections; centralized environment validation and frontend API configuration; correct cookie max-age and auth error handling; schema/controller validation; atomic or transactional follow/like updates; media validation and consistent Cloudinary handling; paginated indexed feed queries; API tests for auth, authorization, and relationship consistency; and production deployment configuration for CORS, static assets, HTTPS, and secrets.

## 12. Source map

- Server startup and middleware: `backend/server.js`
- Authentication flow: `backend/controller/auth.controller.js`, `backend/middleware/protectRoute.js`, `backend/utils/generateToken.js`
- Persistence schemas: `backend/models/`
- API declarations: `backend/routes/`
- Core UI routes and bootstrapping: `frontend/src/App.jsx`, `frontend/src/main.jsx`
- Feed and post interactions: `frontend/src/page/home/`, `frontend/src/components/common/Post.jsx`, `frontend/src/components/common/Posts.jsx`
- Profile and mutations: `frontend/src/page/profile/`, `frontend/src/hooks/`
