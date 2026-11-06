import express from "express"
import {protectRoute} from "../middleware/protectRoute.js"
import {createpost,
    deletepost,
    commentOnPost,
    likeUnlikePost,
    getAllPosts,
    getFollowingPosts,
    getUserPost,
    getLikedPosts} from "../controller/post.controller.js";
const router=express.Router();

router.get("/following",protectRoute,getFollowingPosts)
router.get("/likes/:id",protectRoute,getLikedPosts);
router.get("/all",protectRoute,getAllPosts);
router.get("/user/:userName",protectRoute,getUserPost)
router.post("/create",protectRoute,createpost);
router.post("/like/:id",protectRoute,likeUnlikePost);
router.post("/comment/:id",protectRoute,commentOnPost);
router.delete("/:id",protectRoute,deletepost);

export default router;

