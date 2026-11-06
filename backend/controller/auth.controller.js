import User from "../models/user.model.js";
import bcrypt from "bcrypt";
import generateToken from "../utils/generateToken.js";

export const signup = async (req, res) => {
  try {
    const { userName, fullName, email, password } = req.body;

    // Check if all required fields are present
    if (!userName || !fullName || !email || !password) {
      return res.status(400).json({ error: "All fields are required" });
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: "Invalid email format" });
    }

    // Check for existing user/email
    const existingEmail = await User.findOne({ email });
    const existingUsername = await User.findOne({ userName });
    if (existingEmail || existingUsername){
      return res
        .status(400)
        .json({ error: "Username or Email already exists" });
    }

    // Check password length
    if (password.length < 6) {
      return res
        .status(400)
        .json({ error: "Password must be at least 6 characters long" });
    }

    // Hash the password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    // Create the new user
    const newUser = new User({
      userName,
      fullName,
      email,
      password: hashedPassword,
    });

    // Save to DB first
    await newUser.save();

    // Generate token after successful save
    generateToken(newUser._id, res);

    // Send response
    res.status(201).json({
      _id: newUser._id,
      userName: newUser.userName,
      fullName: newUser.fullName,
      email: newUser.email,
      followers: newUser.followers,
      following: newUser.following,
      profileImg: newUser.profileImg,
      coverImg: newUser.coverImg,
      bio: newUser.bio,
      link: newUser.link,
    });
  } catch (error) {
    console.error("Error in signUp controller:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

export const login = async (req, res) => {
  try {
    const { userName, password } = req.body;

    if (!userName || !password) {
      return res.status(400).json({ error: "Username and password required" });
    }

    const user = await User.findOne({ userName });
    const isPasswordCorrect = await bcrypt.compare(
      password,
      user?.password || ""
    );

    if (!user || !isPasswordCorrect) {
      return res.status(400).json({ error: "Invalid username or password" });
    }

    
    const token = generateToken(user._id, res); 
    
    res.status(200).json({
      _id: user._id,
      userName: user.userName,
      fullName: user.fullName,
      email: user.email,
      followers: user.followers,
      following: user.following,
      profileImg: user.profileImg,
      coverImg: user.coverImg,
      bio: user.bio,
      link: user.link,
    });
  } catch (error) {
    console.log(`Error in login controller: ${error}`);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

export const logout = async (req, res) => {
  try {
    res.cookie("jwt", "", { maxAge: 0 });
    res.status(200).json({ message: "Logged out successfully" });
  } catch (error) {
    console.log(`Error in logout controller: ${error}`);
    res.status(500).json({ error: "Internal Server Error" });
  }
};

export const getme = async (req, res) => {
  try {
    const user = await User.findById(req.user._id).select("-password");
    res.status(200).json(user);
  } catch (error) {
    console.log(`Error in getme controller: ${error}`);
    res.status(500).json({ error: "Internal Server Error" });
  }
};
