import User from "../models/user.model.js";
import cloudinary from "cloudinary";
import Post from "../models/post.model.js";
import Notification from "../models/notification.model.js";

// Create a new post (text or image)
export const createpost = async (req, res) => {
  try {
    const { text } = req.body;
    let { img } = req.body; // base64 or URL
    const userId = req.user._id.toString();

    // Verify user existence
    const user = await User.findById(userId);
    if (!user) {
      return res.status(400).json({ error: "User not found" });
    }

    // Validate input has text or image
    if (!text && !img) {
      return res.status(400).json({ error: "Post must have text or image" });
    }

    // Upload image to Cloudinary if present
    if (img) {
      try {
        const uploadedResponse = await cloudinary.uploader.upload(img);
        img = uploadedResponse.secure_url;
      } catch (err) {
        console.error("Cloudinary upload failed:", err);
        return res.status(500).json({ error: "Image upload failed" });
      }
    }

    // Create and save post document
    const newPost = new Post({
      user: userId,
      text,
      img,
    });
    await newPost.save();

    res.status(201).json(newPost);
  } catch (error) {
    console.error("Error in createpost controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Delete existing post by ID with authorization and image removal
export const deletepost = async (req, res) => {
  try {
    const post = await Post.findById(req.params.id);
    if (!post) return res.status(404).json({ error: "Post not found" });

    if (post.user.toString() !== req.user._id.toString())
      return res.status(401).json({ error: "Not authorized to delete this post" });

    if (post.img) {
      const publicId = post.img.split("/").pop().split(".")[0];
      await cloudinary.uploader.destroy(publicId);
    }

    await Post.findByIdAndDelete(req.params.id);
    return res.status(200).json({ message: "Post deleted successfully" });
  } catch (error) {
    console.error("Error in deletepost controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Add comment to post
export const commentOnPost = async (req, res) => {
  try {
    const { text } = req.body;
    const postId = req.params.id;
    const userId = req.user._id;
    if (!text) return res.status(400).json({ error: "Text field is required" });

    const post = await Post.findById(postId);
    if (!post) return res.status(404).json({ error: "Post not found" });

    post.comments.push({ user: userId, text });
    await post.save();

    res.status(200).json(post);
  } catch (error) {
    console.error("Error in commentOnPost controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Like or unlike post toggle with notification creation
export const likeUnlikePost = async (req, res) => {
  try {
    const userId = req.user._id;
    const postId = req.params.id;

    const post = await Post.findById(postId);
    if (!post) return res.status(404).json({ error: "Post not found" });

    const liked = post.likes.includes(userId);
    if (liked) {
      await Post.updateOne({ _id: postId }, { $pull: { likes: userId } });
      await User.updateOne({ _id: userId }, { $pull: { likedPosts: postId } });
      const updatedLikes = post.likes.filter(id => id.toString() !== userId.toString());
      res.status(200).json(updatedLikes);
    } else {
      post.likes.push(userId);
      await User.updateOne({ _id: userId }, { $push: { likedPosts: postId } });
      await post.save();

      const notification = new Notification({
        from: userId,
        to: post.user,
        type: "like",
      });
      await notification.save();

      res.status(200).json(post.likes);
    }
  } catch (error) {
    console.error("Error in likeUnlikePost controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Get all posts with user and comments populated
export const getAllPosts = async (req, res) => {
  try {
    const posts = await Post.find()
      .sort({ createdAt: -1 })
      .populate({ path: "user", select: "-password" })
      .populate({
        path: "comments.user",
        select: "-password -email -following -followers -bio -link",
      });

    res.status(200).json(posts.length ? posts : []);
  } catch (error) {
    console.error("Error in getAllPosts controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Get posts liked by specified user
export const getLikedPosts = async (req, res) => {
  const userId = req.params.id;
  try {
    const user = await User.findById(userId);
    if (!user) return res.status(404).json({ error: "User not found" });

    const likedPosts = await Post.find({ _id: { $in: user.likedPosts } })
      .populate({ path: "user", select: "-password" })
      .populate({ path: "comments.user", select: "-password" });

    res.status(200).json(likedPosts);
  } catch (error) {
    console.error("Error in getLikedPosts controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Get posts from users the authenticated user is following
export const getFollowingPosts = async (req, res) => {
  const userId = req.user._id;
  try {
    const user = await User.findById(userId);
    if (!user) return res.status(404).json({ error: "User not found" });

    const following = user.following;

    const feedPosts = await Post.find({ user: { $in: following } })
      .sort({ createdAt: -1 })
      .populate({ path: "user", select: "-password" })
      .populate({ path: "comments.user", select: "-password" });

    res.status(200).json(feedPosts);
  } catch (error) {
    console.error("Error in getFollowingPosts controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};

// Get posts by username
export const getUserPost = async (req, res) => {
  try {
    const { userName } = req.params;
    const user = await User.findOne({ userName });
    if (!user) return res.status(404).json({ error: "User not found" });

    const posts = await Post.find({ user: user._id })
      .sort({ createdAt: -1 })
      .populate({ path: "user", select: "-password" });

    res.status(200).json(posts);
  } catch (error) {
    console.error("Error in getUserPost controller:", error);
    res.status(500).json({ error: "Internal server error" });
  }
};
