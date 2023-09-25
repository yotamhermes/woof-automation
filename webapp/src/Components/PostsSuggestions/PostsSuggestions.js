import { useState } from "react";
import { getPostsSuggestions } from "../../Services/postSuggestions";
import PostSuggestionsUi from "./PostSuggestionUI";

function PostsSuggestions() {
  const postsSuggestions = getPostsSuggestions();

  return (
    <div>
      {postsSuggestions.map((postSuggestion) => (
        <PostSuggestions
          key={postSuggestion.suggestion_id}
          initialImages={postSuggestion.images}
          captions={postSuggestion.captions}
        />
      ))}
    </div>
  );
}

function PostSuggestions({ initialImages, captions, suggestion_id }) {
  const [captionIndex, changeIndex] = useState(0);
  const [images, updateImages] = useState(initialImages);

  const handleRemoveImages = (removedImage) => {
    updateImages(images.filter((image) => image !== removedImage));
  };

  const handleCaptionIndexChange = (captionIndex) => {
    changeIndex(captionIndex);
  };

  return (
    <div>
      <PostSuggestionsUi
        key={suggestion_id}
        images={images}
        captions={captions}
        selectedCaptionIndex={captionIndex}
        onChooseCaption={handleCaptionIndexChange}
        onRemoveImage={handleRemoveImages}
        onPost={() => {
          console.log(images);
          console.log(captions[captionIndex]);
        }}
      />
    </div>
  );
}

export default PostsSuggestions;
