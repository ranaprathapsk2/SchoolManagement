from rest_framework import serializers
from accounts.models import Librarian, User
from django.contrib.auth import authenticate


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


class LibrarianSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Librarian
        fields = ['id', 'user', 'librarian_id']

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
    

class LibrarianLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(username=email, password=password)

        if user is None:
            try:
                user = User.objects.get(email=email)
                raise serializers.ValidationError("Incorrect password.")
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")
        try:
            librarian = Librarian.objects.get(user=user)
        except Librarian.DoesNotExist:
            raise serializers.ValidationError("User is not a Librarian.")
        
        if not user.is_librarian:
            raise serializers.ValidationError("You must be a Librarian to log in.")        

        return {'user': user, 'librarian': librarian}
