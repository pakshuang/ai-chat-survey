import React, { useEffect, useState } from 'react';
import { useToast } from '@chakra-ui/react';

const ResumeSnackbar = ({ answers }) => {
    const toast = useToast();


    useEffect(() => {
        if (answers.length>0) {
            toast({
                title: 'Survey resumed from where you left off.',
                status: 'info',
                duration: 3000,
                isClosable: true,
                position: 'bottom-left',
            });
        }
    }, []);

    return null;
};

export default ResumeSnackbar;
