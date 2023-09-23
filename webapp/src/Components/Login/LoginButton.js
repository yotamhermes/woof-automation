import { Button, Box } from "@chakra-ui/react";

function Login({ onClick }) {
  return (
    <Box display="flex" justifyContent="center" alignItems="center" margin={24}>
      <Button onClick={onClick} colorScheme="facebook" size='lg'>
        Login With Facebook
      </Button>
    </Box>
  );
}

export default Login;
