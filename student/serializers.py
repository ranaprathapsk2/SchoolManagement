from rest_framework import serializers
from accounts.models import User, Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'is_student', 'is_officestaff', 'is_librarian', 'date_of_birth', 'remarks', 'is_superuser', 'created_at']
    
    # creating password automatily for users. using name and dob
    def create(self, validated_data):
        full_name = validated_data.get('full_name')
        date_of_birth = validated_data.get('date_of_birth')        
        str_date_of_birth = str(date_of_birth)
        removed_dash_from_dob = str_date_of_birth.replace("-", "")
        removed_spaces_from_name = full_name.replace(" ", "")

        password = f"{removed_spaces_from_name}{removed_dash_from_dob}"

        user = User(**validated_data)       
        user.set_password(password) 
        user.save()

        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'studnet_class', 'student_division', 'address']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)

        # Update the Student instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If user data is provided, update the related User instance
        if user_data:
            user_serializer = UserSerializer(instance=instance.user, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()  # Save the updated user data
            else:
                raise serializers.ValidationError("Invalid user data")

        # Save the updated Student instance
        instance.save()
        return instance
