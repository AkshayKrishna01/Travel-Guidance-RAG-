import Notification from "../models/notification.model.js";
import User from "../models/user.model.js";
import  mongoose  from "mongoose";
import cloudinary from "cloudinary";
import bcrypt from "bcrypt"
export const getProfile=async(req,res)=>{
    try{
        const {userName}=req.params;
        const user=await User.findOne({userName})

        if(!user){
            return res.status(400).json({error:"User not found"})
        }res.status(200).json(user);
    }
    catch(error){
        console.log(`Error in get user profile controller:${error}`)
        res.status(500).json({error:"Internal Server Error"})
    }
}

export const followUnFollowUser=async(req,res)=>{
    try{
        const {id}=req.params;
        const userToModify=await User.findById({_id:id})
        const currentUser=await User.findById({_id:req.user._id})

        if(id===req.user._id){
            return res.status(400).json({error:"You cannot follow or unfollow yourself"})
        }
        if(!userToModify||!currentUser){
            return res.status(400).json({error:"User not found"})
        }
        const isFollowing =currentUser.following.includes(id);
        
        if(isFollowing){
            await User.findByIdAndUpdate({_id:id},{$pull:{followers:req.user._id}})
            await User.findByIdAndUpdate({_id: req.user._id},{$pull:{following:id}})
            res.status(200).json({message:"Unfollow Successfully"})
        }
        else{
            await User.findByIdAndUpdate({_id:id},{$push:{followers:req.user._id}})
            await User.findByIdAndUpdate({_id:req.user._id},{$push:{following:id}})
            const newNotification=new Notification({
                type:"follow",
                from:req.user._id,
                to:userToModify._id
            })
            await newNotification.save()
            res.status(200).json({message:"follow Successfully"})

        }
    }
    catch(error){
        console.log(`Error in follow and Unfollow controller ${error}`)
        res.status(500).json({error:"Internal server error"})
    }
}
export const suggestion=async(req,res)=>{
    try{
        const userId=req.user._id;
        const userFollowedByMe=await User.findById({_id:userId}).select("-password");
        const users=await User.aggregate([
            {
                $match:{
                    _id:{$ne:userId}
                }
            },{
                $sample:{
                    size:10
                }
            }
        ])
        const filteredUser=users.filter((user)=>!userFollowedByMe.following.includes(user._id))
        const suggestedUser=filteredUser.slice(0,4);
        suggestedUser.forEach((user)=>{user.password=null})

        res.status(200).json({suggestedUser});
    }
    catch(error){
        console.log(`Error in suggestion controller ${error}`)
        res.status(500).json({error:"Internal server error"})
    }}
export const updateuser=async(req,res)=>{
    try{
        let userid=req.user._id;
        let{userName,fullName,email,currentpassword,newpassword,bio,link}=req.body;
        let{profileImg,coverImg}=req.body;
        let user=await User.findById({_id:userid})
        if(!user){
            return res.status(400).json({error:"User not Found"})
        }
        if((!newpassword&&currentpassword)||(newpassword&&!currentpassword)){
            return res.status(400).json({error:"please Provide password"})        }
        if(currentpassword&&newpassword){
            const isMatch=await bcrypt.compare(currentpassword,user.password)
            if(!isMatch){
                return res.status(400).json({error:"Cuurent password is Incorrect"})
            }if(newpassword.length<6){
                return res.status(400).json({error:"Password Must Have atleast 6 Character"})
            }
            const salt=await bcrypt.genSalt(10);
            user.password=await bcrypt.hash(newpassword,salt);
        }
        // if(profileImg){
        //     if(user.profileImg){
        //         await cloudinary.uploader.destroy(user.profileImg.split("/").pop().split(".")[0])
        //     }
        //     const uploadedResponse=await cloudinary.uploader.upload(profileImg);
        //     profileImg =uploadedResponse.secure_url;
        // }
        // if(coverImg){
        //     if(user.coverImg){
        //         await cloudinary.uploader.destroy(user.coverImg.split("/").pop().split(".")[0])
        //     }
        //     const uploadedResponse=await cloudinary.uploader.upload(coverImg);
        //     profileImg =uploadedResponse.secure_url;
        // }
        user.fullName=fullName||user.fullName
        user.email=email||user.email;
        user.userName=userName||user.userName
        user.bio=bio||user.bio;
        user.link=link||user.link;
        user.profileImg=profileImg||user.profileImg;
        user.coverImg=coverImg||user.coverImg
        user=await user.save();
        user.password=null;
        return res.status(200).json(user);
    }
    catch(error){
        console.log(`Error in updateuser controller ${error}`)
        res.status(500).json({error:"Internal server error"})
    }
}
