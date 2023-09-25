import { Box, Image, Text, Flex, IconButton } from "@chakra-ui/react";
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from "react-responsive-carousel";
import { DeleteIcon } from "@chakra-ui/icons";
import styles from "./styles.module.css";

function PostSuggestions({
  images,
  caption,
  onPost,
  onDelete,
  onRemoveImage,
  onChooseCaption,
}) {
  return (
    <Box
      maxW="sm"
      borderWidth="1px"
      borderRadius="lg"
      overflow="hidden"
      boxShadow="lg"
      margin={5}
    >
      <Carousel showThumbs={false}>
        {images.map((image) => (
          <div className={styles.imageContainer}>
            <Image src={image} key={image} />
            <IconButton
              onClick={onRemoveImage}
              className={styles.deleteIcon}
              isRound={true}
              variant="solid"
              color="rgba(0, 0, 0, 0.8)"
              aria-label="Remove"
              fontSize="20px"
              icon={<DeleteIcon />}
            />
          </div>
        ))}
      </Carousel>

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
