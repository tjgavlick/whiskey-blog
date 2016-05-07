# Whiskey Blog

This is a personal venture that I'm using to learn some new stuff. As of now, I'm aiming for a simple writing platform for booze reviews. It should do as much to not impede my writing workflow as possible, and it should offer ways for other people to find stuff they like.

Initial thoughts on software are Python 3.x, Flask, Postgres, SQLAlchemy, and nginx, but we'll see if that holds true.

Right now it has a front-facing UI and an admin area. It can save and list reviews, articles, distilleries, and locales. It can do simple multifaceted filtering on reviews. I'd like to …

- [x] Move my db to postgres
- [x] Extend articles and reviews to show related items
- [x] Make the admin interface prettier and more useful
- [x] Add auth for admin access
- [x] Add live markdown previews for editing
- [x] Add image upload
- [x] Add an asset browser/selector
- [ ] Implement keyword search
- [x] Serve it with nginx and set up a local Vagrant or Docker environment for development
- [ ] Launch the damn thing

---

Manual tasks upon deployment:

- compile sass
- specify production config in app/__init__py
- change db user/pass in both the db Dockerfile and the app config
- change secret key in the app config

---

MIT license. Please let me know if you use some part of this, as well as give credit on the work itself. It's a nice thing to do!

