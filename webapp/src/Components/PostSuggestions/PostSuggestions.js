import { getPostsSuggestions } from "../../Services/postSuggestions";
import PostSuggestionsUi from "./PostSuggestionUI";

function PostSuggestions() {
  const postsSuggestions = getPostsSuggestions();

  return (
    <div>
      {postsSuggestions.map((postSuggestion) => (
        <PostSuggestionsUi {...postSuggestion} />
      ))}
    </div>
  );
}

export default PostSuggestions;
