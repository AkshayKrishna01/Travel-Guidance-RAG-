import express from "express";
const router=express.Router();
import {protectRoute} from "../middleware/protectRoute.js";
import {signup,login,logout,getme} from "../controller/auth.controller.js";
router.post("/signup",signup)
router.post("/login",login)
router.post("/logout",logout)
router.get("/me",protectRoute,getme)

export default router;
