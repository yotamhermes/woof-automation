import { getPostsSuggestions } from "../../Services/postSuggestions";
import PostSuggestionsUi from "./PostSuggestionUI";

function PostSuggestions() {
  const postsSuggestions = getPostsSuggestions();

  return (
    <div>
      {postsSuggestions.map((postSuggestion) => (
        <PostSuggestionsUi
          key={postSuggestion.suggestion_id}
          {...postSuggestion}
          caption={postSuggestion.captions[0]}
        />
      ))}
    </div>
  );
}

export default PostSuggestions;
