import Post from "./Post";
import PostSkeleton from "../skeletons/PostSkeleton";
import { baseUrl } from "../../constant/url";
import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

const Posts = ({ feedType,userName,userId}) => {
  // Get endpoint based on feedType
  const getPostEndPoint = () => {
    switch (feedType) {
      case "forYou":
        return `${baseUrl}/api/posts/all`;
      case "following":
        return `${baseUrl}/api/posts/following`;
      case "posts":
        return `${baseUrl}/api/posts/user/${userName}`;
      case "likes":
        return `${baseUrl}/api/posts/likes/${userId}`;
      default:
        return `${baseUrl}/api/posts/all`;
    }
  };

  const POST_ENDPOINT = getPostEndPoint();

  // Fetch posts
  const {
    data: posts,
    isLoading,
    refetch,
    isRefetching,
  } = useQuery({
    queryKey: ["posts", feedType], // include feedType in key for auto-refetch
    queryFn: async () => {
      try {
        const res = await fetch(POST_ENDPOINT, {
          method: "GET",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.error || "Something went wrong");
        }

        return data;
      } catch (error) {
        throw new Error(error.message || "Something went wrong");
      }
    },
  });

  // Refetch on feedType change
  useEffect(() => {
    refetch();
  }, [feedType, refetch]);

  return (
    <>
      {(isLoading || isRefetching) && (
        <div className="flex flex-col justify-center">
          <PostSkeleton />
          <PostSkeleton />
          <PostSkeleton />
        </div>
      )}

      {!isLoading && posts?.length === 0 && (
        <p className="text-center my-4">No posts in this tab. Switch 👻</p>
      )}

      {!isLoading && posts && posts.length > 0 && (
        <div>
          {posts.map((post) => (
            <Post key={post._id} post={post} />
          ))}
        </div>
      )}
    </>
  );
};

export default Posts;
