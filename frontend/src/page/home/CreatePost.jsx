import { CiImageOn } from "react-icons/ci";
import { BsEmojiSmileFill } from "react-icons/bs";
import { useRef, useState } from "react";
import { IoCloseSharp } from "react-icons/io5";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { baseUrl } from "../../constant/url";
import LoadingSpinner from "../../components/common/LoadingSpinner";

// Fetch currently logged-in user data
const fetchAuthUser = async () => {
  const res = await fetch(`${baseUrl}/api/auth/me`, {
    credentials: "include",
  });
  if (!res.ok) {
    const errData = await res.json();
    throw new Error(errData.error || "Failed to fetch user data");
  }
  return res.json();
};

const CreatePost = () => {
  const [text, setText] = useState("");
  const [img, setImg] = useState(null);
  const imgRef = useRef(null);

  // Fetch auth user data with caching and error/loading states
  const { data: authUser, isLoading, error } = useQuery({
    queryKey: ["authUser"],
    queryFn: fetchAuthUser,
    staleTime: 5 * 60 * 1000, // cache for 5 minutes
  });

  const queryClient = useQueryClient();

  // Mutation to create a new post
  const { mutate: createPost, isLoading: isPending, isError } = useMutation({
    mutationFn: async ({ text, img }) => {
      const res = await fetch(`${baseUrl}/api/posts/create`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, img }),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Something went wrong");
      }
      return data;
    },
    onSuccess: () => {
      setImg(null);
      setText("");
      toast.success("Post Created Successfully");
      queryClient.invalidateQueries({ queryKey: ["posts"] }); // refresh posts cache
    },
  });

  // Handle post form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Validate non-empty post text or image
    if (!text.trim() && !img) {
      toast.error("Post cannot be empty!");
      return;
    }
    createPost({ text, img });
  };

  // Convert uploaded file to base64 string
  const handleImgChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setImg(reader.result);
    reader.readAsDataURL(file); // converts file to base64 data URL
  };

  if (isLoading) return <LoadingSpinner size="sm" />;
  if (error) return <div className="text-red-500">Failed to load user data.</div>;

  return (
    <div className="flex p-4 items-start gap-4 border-b border-gray-700">
      <div className="avatar">
        <div className="w-8 rounded-full">
          <img
            src={authUser?.profileImg || "/avatar-placeholder.png"}
            alt="Profile"
          />
        </div>
      </div>
      <form className="flex flex-col gap-2 w-full" onSubmit={handleSubmit}>
        <textarea
          className="textarea w-full p-0 text-lg resize-none border-none focus:outline-none border-gray-800"
          placeholder="What is happening?!"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        {img && (
          <div className="relative w-72 mx-auto">
            <IoCloseSharp
              className="absolute top-0 right-0 text-white bg-gray-800 rounded-full w-5 h-5 cursor-pointer"
              onClick={() => {
                setImg(null);
                imgRef.current.value = null;
              }}
            />
            <img
              src={img}
              className="w-full mx-auto h-72 object-contain rounded"
              alt="Post preview"
            />
          </div>
        )}
        <div className="flex justify-between border-t py-2 border-t-gray-700">
          <div className="flex gap-1 items-center">
            <CiImageOn
              className="fill-primary w-6 h-6 cursor-pointer"
              onClick={() => imgRef.current.click()}
            />
            <BsEmojiSmileFill className="fill-primary w-5 h-5 cursor-pointer" />
          </div>
          <input type="file" hidden ref={imgRef} onChange={handleImgChange} />
          <button className="btn btn-primary rounded-full btn-sm text-white px-4">
            {isPending ? <LoadingSpinner size="sm" /> : "Post"}
          </button>
        </div>
        {isError && <div className="text-red-500">Something went wrong</div>}
      </form>
    </div>
  );
};

export default CreatePost;
