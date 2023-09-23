import { Box, Image, Text, Flex } from "@chakra-ui/react";

function PostSuggestions({ image, caption, onPost, onDelete }) {
  return (
    <Box
      maxW="sm"
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      boxShadow="lg"
      margin={5}
    >
      <Image src={image} />

      <Box p="6">
        <Text mt={4} textAlign="center">
          {caption}
        </Text>
      </Box>
      <Flex>
        <Box
          as="button"
          p="6"
          display="flex"
          justifyContent="center"
          alignItems="center"
          bg="blue.500"
          flexGrow="1"
          onClick={onPost}
        >
          <Text fontWeight="bold">Post</Text>
        </Box>
        <Box
          as="button"
          p="6"
          display="flex"
          justifyContent="center"
          alignItems="center"
          bg="red.600"
          onClick={onDelete}
        >
          <Text fontWeight="bold">Delete</Text>
        </Box>
      </Flex>
    </Box>
  );
}

export default PostSuggestions;
