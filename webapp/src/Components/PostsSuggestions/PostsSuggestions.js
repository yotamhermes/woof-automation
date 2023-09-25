import { useEffect, useState } from "react";
import {
  getPostsSuggestions,
  markPostsAsDone,
} from "../../Services/PostSuggestions.js";
import PostSuggestionsUi from "./PostSuggestionUI";

function PostsSuggestions() {
  const [postsSuggestions, updatePostSuggestions] = useState([]);

  useEffect(() => {
    getPostsSuggestions().then((res) => updatePostSuggestions(res));
  }, []);

  return (
    <div>
      {postsSuggestions.map((postSuggestion) => (
        <PostSuggestions
          key={postSuggestion.created_from_prompt}
          initialImages={postSuggestion.images}
          captions={postSuggestion.captions}
          created_from_prompt={postSuggestion.created_from_prompt}
        />
      ))}
    </div>
  );
}

function PostSuggestions({ initialImages, captions, created_from_prompt }) {
  const [captionIndex, changeIndex] = useState(0);
  const [images, updateImages] = useState(initialImages);

  const handleRemoveImages = (removedImage) => {
    updateImages(images.filter((image) => image !== removedImage));
  };

  const handleCaptionIndexChange = (captionIndex) => {
    changeIndex(captionIndex);
  };

  const handlePost = () => {
    console.log(images);
    console.log(captions[captionIndex]);

    markPostsAsDone(created_from_prompt);
  };

  return (
    <div>
      <PostSuggestionsUi
        images={images}
        captions={captions}
        selectedCaptionIndex={captionIndex}
        onChooseCaption={handleCaptionIndexChange}
        onRemoveImage={handleRemoveImages}
        onPost={handlePost}
      />
    </div>
  );
}

export default PostsSuggestions;
