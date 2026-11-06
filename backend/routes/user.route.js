import express from "express"
import {protectRoute} from "../middleware/protectRoute.js"
import {getProfile, followUnFollowUser, suggestion, updateuser} from "../controller/user.controller.js";
const router=express.Router();

router.get("/profile/:userName",protectRoute,getProfile)
router.post("/follow/:id",protectRoute,followUnFollowUser)
router.get("/suggested",protectRoute,suggestion)
router.post("/update",protectRoute,updateuser)
export default router;