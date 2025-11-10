# 📱 Network – A Social Network App (CS50W Project 4)

This is **Project 4** from **CS50’s Web Programming with Python and JavaScript** course — a social network web application built using **Django**, **HTML**, **CSS**, and **JavaScript**.  
The platform allows users to post content, follow others, like/unlike posts, and edit their own posts dynamically.

---

## 🚀 Features

### 📝 1. New Post
- Logged-in users can create new text-based posts.
- Posts are timestamped and displayed in reverse chronological order.
- Posts can be submitted via a text area on the “All Posts” page or a separate page.

### 🌐 2. All Posts Page
- Displays all posts from all users.
- Shows each post’s:
  - Author (clickable to view their profile)
  - Content
  - Timestamp
  - Like count
- Supports pagination (10 posts per page).

### 👤 3. Profile Page
- Displays:
  - User’s posts (most recent first)
  - Number of followers and following
- Logged-in users can **Follow/Unfollow** others.
- Users cannot follow themselves.

### ❤️ 4. Like / Unlike System
- Users can like or unlike any post.
- Like count updates asynchronously (using `fetch` and JavaScript) without reloading the page.

### ✏️ 5. Edit Post
- Users can edit **only their own posts**.
- Edit mode replaces post content with a `textarea` and **Save/Cancel** buttons.
- Saving updates the content dynamically via `fetch` without reloading the page.

### 👥 6. Following Page
- Shows all posts made by users that the logged-in user follows.
- Paginated just like the “All Posts” page.
- Available only for authenticated users.

### 🔄 7. Pagination
- Implemented via Django’s `Paginator` class.
- “Next” and “Previous” buttons appear automatically when applicable.

---

## 🧰 Technologies Used
- **Django** (Python)
- **SQLite3** (Database)
- **HTML5**, **CSS3**, **Bootstrap**
- **JavaScript (ES6)** – for fetch requests and DOM manipulation
- **Django Paginator** – for post pagination

---

## ▶️ Running the App

### 1. Clone Repository
```bash
git clone https://github.com/tasamidinov/project4-network.git
cd project4
