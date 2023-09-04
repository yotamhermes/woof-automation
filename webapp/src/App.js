import PostSuggestions from './Components/PostSuggestions/PostSuggestions'
import { ChakraProvider } from '@chakra-ui/react'

function App() {
  return (
    <ChakraProvider>
      <PostSuggestions />
    </ChakraProvider>
  );
}

export default App;
